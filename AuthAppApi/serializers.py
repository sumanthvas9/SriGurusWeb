from django.utils.encoding import force_text
from rest_framework import serializers, status
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import APIException

from AuthApp.custom.email import EmailHandling
from AuthApp.models import EmailDirectory, EMAIL_TYPE_CHOICES, UserDetails, Categories, ServiceRequest

UserModel = get_user_model()


class CustomAPIValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            if type(detail) is str:
                errors = []
                res_list = force_text(detail).strip('][').split(', ')
                for res_ind in res_list:
                    errors.append(res_ind.replace("'", ''))
                if errors:
                    self.detail = {'msg': errors[0] + format("\n".join(errors[1:]))}
                else:
                    self.detail = {'msg': errors}
            elif type(detail) is dict:
                self.detail = detail
            else:
                self.detail = {'msg': force_text(self.default_detail)}
        else:
            self.detail = {'msg': force_text(self.default_detail)}


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password', 'name', 'mobile', 'provider_id']
        extra_kwargs = {
            'email': {'required': True, 'error_messages': {'blank': "Please provide Email Id."}},
            'password': {'required': True, 'write_only': True, 'error_messages': {'blank': "Please provide Email Id."}},
            'name': {'required': True, 'error_messages': {'blank': "Please provide Name."}},
            'mobile': {"source": "phoneNumber", 'required': False, 'error_messages': {'blank': "Please provide Phone Number."}},
            "provider_id": {'source': "registeredThrough"}
        }

    @staticmethod
    def validate_password(value):
        # try:
        #     validate_password(value)
        # except ValidationError as exc:
        #     raise CustomAPIValidation(detail=str(exc), field="password", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        return value

    @staticmethod
    def validate_email(value):
        try:
            user_model = UserModel.objects.get(**{'email': value})
            reg_through = user_model.registeredThrough.upper()
            if user_model.otpVerified and (reg_through in ['WEB', 'APP']):
                raise CustomAPIValidation(detail='Account already verified. Please Login.', field="email", status_code=status.HTTP_302_FOUND)
            else:
                raise CustomAPIValidation(detail='User already registered through ' + reg_through + '.\nPlease Login.', field="email",
                                          status_code=status.HTTP_302_FOUND)
                # token, _ = Token.objects.get_or_create(user=user_model)
                # raise CustomAPIValidation(detail={"sriguru_token": token.key, "otp_verified": "No", "msg": "Please verify your account."},
                #                           field="email", status_code=310)
        except UserModel.DoesNotExist:
            pass
        return value

    @staticmethod
    def validate_mobile(value):
        try:
            UserModel.objects.get(**{'phoneNumber': value})
            raise CustomAPIValidation(detail='Phone Number already exists.', field="mobile", status_code=status.HTTP_302_FOUND)
        except UserModel.DoesNotExist:
            pass
        return value

    def validate(self, attrs):
        validated_data = super(RegisterSerializer, self).validate(attrs=attrs)
        error_dict = {}
        if error_dict:
            raise serializers.ValidationError(error_dict)
        return validated_data

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data.get('email'),
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            phoneNumber=validated_data.get('phoneNumber'),
            registeredThrough="APP" if validated_data.get('registeredThrough') is None else validated_data.get('registeredThrough'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop("domain")
        super(LoginSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def validate_password(value):
        return value

    def validate_user_name(self, value):
        try:
            user_model = UserModel.objects.get(**{'email': value})
            if not user_model.otpVerified:
                email_handling = EmailHandling()
                email_handling.send_email(email_type="Resend", user=user_model, domain=self.domain)
                raise CustomAPIValidation(detail='Please verify your account.', field="email", status_code=310)
        except UserModel.DoesNotExist:
            raise CustomAPIValidation(detail="User does not exist.", field="email", status_code=status.HTTP_404_NOT_FOUND)
        return value

    def validate(self, attrs):
        validated_data = super(LoginSerializer, self).validate(attrs=attrs)
        self.user = authenticate(username=validated_data.get('user_name'), password=validated_data.get('password'))
        if not self.user:
            raise CustomAPIValidation(detail="Invalid credentials provided.", field="password", status_code=status.HTTP_403_FORBIDDEN)
        if not self.user.is_active:
            raise CustomAPIValidation(detail="User is inactive.", field="password", status_code=status.HTTP_403_FORBIDDEN)
        return validated_data

    def update(self, instance, validated_data):
        return self.user

    def create(self, validated_data):
        return self.user


class ForgotPasswordSerializer(serializers.ModelSerializer):
    user_obj = UserModel.objects.all()
    type = serializers.ChoiceField(choices=('init', 'submit'))
    email_id = serializers.EmailField()
    password = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop("domain")
        super(ForgotPasswordSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = EmailDirectory
        fields = ['email_id', 'type', 'otp', 'password']
        extra_kwargs = {
            'email_id': {'required': True, 'error_messages': {'blank': "Email Id is mandatory."}},
            'type': {'required': True, 'error_messages': {'blank': "Type is mandatory."}},
            'otp': {'source': 'otpCode', 'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate(self, attrs):
        validated_data = super(ForgotPasswordSerializer, self).validate(attrs=attrs)
        fp_type = validated_data.get('type', None)
        try:
            self.user = UserModel.objects.get(email=validated_data['email_id'])
        except UserModel.DoesNotExist:
            raise CustomAPIValidation(detail="Invalid email id provided", field="password", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        if self.user.registeredThrough.upper() not in ['WEB', 'APP']:
            raise CustomAPIValidation(detail="Forgot password not allowed for accounts registered through social login", field="email_id",
                                      status_code=status.HTTP_403_FORBIDDEN)
        if fp_type == 'init':
            pass
        elif fp_type == 'submit':
            error_dict = []
            password = validated_data.get('password', None)
            if not password:
                error_dict.append("Password is mandatory")
            otp_code = validated_data.get('otpCode', None)
            if not otp_code:
                error_dict.append("OTP is mandatory")
            if error_dict:
                raise CustomAPIValidation(detail=str(error_dict), field="password", status_code=status.HTTP_406_NOT_ACCEPTABLE)
            email_dir_obj = EmailDirectory.objects.filter(user=self.user, isActive=True, type='ForgotPassword')
            otp_code_query_set = email_dir_obj.values('otpCode')
            if otp_code_query_set and otp_code_query_set[0]['otpCode'] != validated_data.get('otpCode'):
                error_dict = "Incorrect OTP code"
            if error_dict:
                raise CustomAPIValidation(detail=error_dict, field="password", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        return validated_data

    def create(self, validated_data):
        fp_type = validated_data.get('type', None)
        if fp_type == 'init':
            email_handling = EmailHandling()
            email_handling.send_email(email_type="ForgotPassword", user=self.user, domain=self.domain)
            return "init"
        else:
            EmailDirectory.objects.filter(user=self.user, isActive=True, type='ForgotPassword').update(isActive=False)
            self.user.password = validated_data['password']
            self.user.save()
            return 'submit'


class OTPResendSerializer(serializers.Serializer):
    email_id = serializers.EmailField(required=True,
                                      error_messages={'blank': "Email Id can not be empty.", 'required': 'Email Id is required.'})
    type = serializers.ChoiceField(required=True, choices=EMAIL_TYPE_CHOICES,
                                   error_messages={'blank': "Type can not be empty.", 'required': 'Type is required.'})

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop("domain")
        super(OTPResendSerializer, self).__init__(*args, **kwargs)

    def validate_email(self, value):
        try:
            UserModel.objects.get(**{'email': value})
        except UserModel.DoesNotExist:
            raise CustomAPIValidation(detail="User does not exist.", field="email", status_code=status.HTTP_404_NOT_FOUND)
        return value

    def validate(self, attrs):
        validated_data = super(OTPResendSerializer, self).validate(attrs=attrs)
        return validated_data

    def create(self, validated_data):
        email_handling = EmailHandling()
        email_handling.send_email(email_type=validated_data.get('type', "Resend"),
                                  user=UserModel.objects.get(**{'email': validated_data.get('email_id')}), domain=self.domain)
        return True

    def update(self, instance, validated_data):
        pass


class OTPValidationSerializer(serializers.Serializer):
    email_id = serializers.EmailField(required=True,
                                      error_messages={'blank': "Email Id can not be empty.", 'required': 'Email Id is required.'})
    type = serializers.ChoiceField(required=True, choices=EMAIL_TYPE_CHOICES,
                                   error_messages={'blank': "Type can not be empty.", 'required': 'Type is required.'})
    otp = serializers.CharField(required=True, error_messages={'blank': "OTP can not be empty.", 'required': 'OTP is required.'})

    @staticmethod
    def validate_email(value):
        try:
            UserModel.objects.get(**{'email': value})
        except UserModel.DoesNotExist:
            raise CustomAPIValidation(detail="User does not exist.", field="email", status_code=status.HTTP_404_NOT_FOUND)
        return value

    def validate(self, attrs):
        validated_data = super(OTPValidationSerializer, self).validate(attrs=attrs)
        query_filter_dict = {'user': UserModel.objects.get(email=validated_data.get('email_id')), 'type': validated_data.get('type'),
                             'otpCode': validated_data.get('otp'), 'isActive': True}
        self.query_set = EmailDirectory.objects.filter(**query_filter_dict).values()
        if not self.query_set:
            raise CustomAPIValidation(detail="Incorrect OTP provided.", field="otp", status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return validated_data

    def create(self, validated_data):
        self.query_set.update(isActive=False)
        UserModel.objects.filter(email=validated_data.get('email_id')).update(otpVerified=True)
        user = UserModel.objects.get(email=validated_data.get('email_id'))
        return user

    def update(self, instance, validated_data):
        pass


USER_DETAILS_KWARGS = {
    'user_dob': {'source': 'dob', 'required': True, 'error_messages': {'blank': "DOB is mandatory.", 'required': "DOB is mandatory."}},
    'gender': {'required': True, 'error_messages': {'blank': "Gender is mandatory.", 'required': "Gender is mandatory."}},
    'address': {'required': True, 'error_messages': {'blank': "Address is mandatory.", 'required': "Address is mandatory."}},
    'city': {'required': True, 'error_messages': {'blank': "City is mandatory.", 'required': "City is mandatory."}},
    'state': {'required': True, 'error_messages': {'blank': "State is mandatory.", 'required': "State is mandatory."}},
    'country': {'required': True, 'error_messages': {'blank': "Country is mandatory.", 'required': "Country is mandatory."}},
    'pincode': {'source': 'zip', 'required': True, 'error_messages': {'blank': "Zip code is mandatory.", 'required': "Pincode is mandatory."}},
}


class UserDetailsSerializer(serializers.ModelSerializer):
    user_obj = UserModel.objects.all()
    user_id = serializers.PrimaryKeyRelatedField(queryset=user_obj, source='user.id')
    name = serializers.CharField(source='user.name', error_messages={'blank': "Name can not be empty.", 'required': 'Name is required.'})
    mobile_no = serializers.CharField(source='user.phoneNumber')
    email_id = serializers.EmailField(source='user.email',
                                      error_messages={'blank': "Email Id can not be empty.", 'required': 'Email Id is required.'})

    class Meta:
        model = UserDetails
        fields = ['user_dob', 'gender', 'address', 'city', 'state', 'country', 'pincode', 'user_id', 'name', 'email_id', 'mobile_no']
        extra_kwargs = USER_DETAILS_KWARGS

    def create(self, validated_data):
        user_detail = UserDetails.objects.create(
            user=validated_data['user']['id'],
            dob=validated_data.get('dob'),
            gender=validated_data.get('gender'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            country=validated_data.get('country'),
            zip=validated_data.get('zip'),
        )
        user_detail.save()
        return user_detail

    def update(self, instance, validated_data):
        instance.dob = validated_data.get('dob')
        instance.gender = validated_data.get('gender')
        instance.address = validated_data.get('address')
        instance.city = validated_data.get('city')
        instance.state = validated_data.get('state')
        instance.country = validated_data.get('country')
        instance.zip = validated_data.get('zip')
        instance.save()
        return instance


class UserDetailsSerializerFromParent(serializers.ModelSerializer):
    # user_details = UserDetailsSerializer(many=True)
    user_details = serializers.SerializerMethodField('_get_children')

    @staticmethod
    def _get_children(obj):
        try:
            serializer = UserDetailsSerializer(UserDetails.objects.get(user=obj), many=False)
            print(serializer.data)
            return serializer.data
        except UserDetails.DoesNotExist as e:
            return {}

    class Meta:
        model = UserModel
        fields = ['name', 'email_id', 'mobile_no', 'user_details']
        extra_kwargs = {
            'email_id': {'source': 'email'},
            'mobile_no': {'source': 'phoneNumber'},
        }


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['cat_id', 'cat_name', 'cat_description', 'tel_name', 'tel_pdf_url', 'hindi_name', 'hindi_pdf_url']
        extra_kwargs = {
            'cat_id': {'source': 'id'},
            'cat_name': {'source': 'catName'},
            'cat_description': {'source': 'catDescription'},
            'tel_name': {'source': 'telName'},
            'tel_pdf_url': {'source': 'telPdfUrl'},
            'hindi_name': {'source': 'hindiName'},
            'hindi_pdf_url': {'source': 'hindiPdfUrl'},
        }


class ServiceRequestNewSerializer(serializers.ModelSerializer):
    user_obj = UserModel.objects.all()
    user_id = serializers.PrimaryKeyRelatedField(queryset=user_obj, source='user.id')

    class Meta:
        model = ServiceRequest
        fields = ['name', 'email_id', 'phone', 'message', 'reply', 'location_type', 'address', 'city', 'state', 'country', 'zip', 'user_id']
        extra_kwargs = {
            'email_id': {'source': 'email', 'required': True, 'error_messages': {'blank': "Email is mandatory.", 'required': "Email is mandatory."}},
            'phone': {'source': 'phoneNumber'},
            'location_type': {'source': 'locationType', 'required': True,
                              'error_messages': {'blank': "Location Type is mandatory.", 'required': "Location Type is mandatory."}}
        }

    def create(self, validated_data):
        service_request = ServiceRequest.objects.create(
            user=validated_data['user']['id'],
            email=validated_data.get('email'),
            phoneNumber=validated_data.get('phoneNumber'),
            message=validated_data.get('message'),
            locationType=validated_data.get('locationType'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            country=validated_data.get('country'),
            zip=validated_data.get('zip'),
        )
        service_request.save()
        return service_request

    def update(self, instance, validated_data):
        pass
