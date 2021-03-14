import traceback

from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators import csrf
from rest_framework import permissions, status, authentication, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response as restResponse

from AuthApp.custom.email import EmailHandling
from AuthApp.models import UserDetails, Categories, ServiceRequest
from AuthAppApi.serializers import RegisterSerializer, LoginSerializer, UserDetailsSerializer, CategoriesSerializer, ServiceRequestNewSerializer, \
    ForgotPasswordSerializer, OTPValidationSerializer

UserModel = get_user_model()

AUTHENTICATION_CLASSES = [authentication.TokenAuthentication,
                          authentication.BasicAuthentication,
                          authentication.SessionAuthentication]


def error_message_handler(dict_data):
    errors = []
    for key, value in dict_data.items():
        res_list = str(value[0]).strip('][').split(', ')
        for res_ind in res_list:
            errors.append(res_ind)
    if errors:
        return errors[0] + format("\n".join(errors[1:]))
    return None


@csrf.csrf_exempt
@api_view(["POST", "GET"])
@permission_classes((permissions.AllowAny,))
@parser_classes([JSONParser])
def token_login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return restResponse(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if not user:
            return restResponse(
                {"error": "Invalid Credentials or user not active"}, status=status.HTTP_403_FORBIDDEN
            )
        if not user.is_active:
            return restResponse(
                {"error": "Customer is not active"}, status=status.HTTP_403_FORBIDDEN
            )
        token, _ = Token.objects.get_or_create(user=user)
        return restResponse(
            {"token": token.key}, status=status.HTTP_200_OK
        )
    except Exception as exception:
        return restResponse({"error": "Provided POST Request"}, status=status.HTTP_400_BAD_REQUEST)


@csrf.csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def customer_registration(request):
    register_serializer = RegisterSerializer(data=request.data)
    if register_serializer.is_valid():
        user = register_serializer.save()
        email_handling = EmailHandling()
        email_handling.send_email(email_type="Registration", user=user, domain=get_current_site(request))
        return restResponse({"otp_verified": "No", "msg": "Please verify your account."}, status=status.HTTP_200_OK)
    else:
        error_string = error_message_handler(register_serializer.errors)
        if error_string:
            return restResponse({"msg": error_string}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return restResponse({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf.csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def customer_login(request):
    login_serializer = LoginSerializer(domain=get_current_site(request), data=request.data)
    if login_serializer.is_valid():
        user = login_serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return restResponse({"sriguru_token": token.key, "otp_verified": "Yes", "msg": "Logged in successfully."}, status=status.HTTP_200_OK)
    else:
        print(login_serializer.errors)
        return restResponse({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes(AUTHENTICATION_CLASSES)
@permission_classes([permissions.IsAuthenticated])
@parser_classes([JSONParser])
def change_password(request):
    user_obj = UserModel.objects.get(id=request.user.id)
    new_password = request.data.get("new_password", "")
    if new_password:
        user_obj.password = new_password
        user_obj.save()
        return restResponse({"msg": "Password changed successfully."}, status=status.HTTP_200_OK)
    return restResponse({"msg": "Password should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(domain=get_current_site(request), data=request.data)
    if serializer.is_valid():
        if serializer.save() == 'init':
            return restResponse({"msg": "OTP sent successfully."}, status=status.HTTP_200_OK)
        else:
            return restResponse({"msg": "Password reset successful."}, status=status.HTTP_200_OK)
    else:
        print(serializer.errors)
        error_string = error_message_handler(serializer.errors)
        if error_string:
            return restResponse({"msg": error_string}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return restResponse({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def resend_auth_otp(request):
    try:
        print(request.data)
        email_handling = EmailHandling()
        email_handling.send_email(email_type=request.data.get('type', "Resend"), user=UserModel.objects.get(), domain=get_current_site(request))
        return restResponse({"msg": "OTP sent successfully."}, status=status.HTTP_200_OK)
    except Exception as error:
        traceback.print_exc()
        return restResponse({"msg": "Internal server occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def auth_otp_validation(request):
    serializer = OTPValidationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return restResponse({"sriguru_token": token.key, "otp_verified": "Yes", "msg": "OTP verified successfully."}, status=status.HTTP_200_OK)
    else:
        error_string = error_message_handler(serializer.errors)
        if error_string:
            return restResponse({"msg": error_string}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return restResponse({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes(AUTHENTICATION_CLASSES)
@permission_classes([permissions.IsAuthenticated])
@parser_classes([JSONParser])
def set_user_info(request):
    request.data['user_id'] = request.user.id
    try:
        user_details = UserDetails.objects.get(user=request.user)
        user_details_serializer = UserDetailsSerializer(user_details, data=request.data)
    except UserDetails.DoesNotExist as error:
        user_details_serializer = UserDetailsSerializer(data=request.data)

    if user_details_serializer.is_valid():
        user_details_serializer.save()
        return restResponse({"msg": "Profile updated successfully."}, status=status.HTTP_200_OK)
    else:
        error_string = error_message_handler(user_details_serializer.errors)
        if error_string:
            return restResponse({"msg": error_string}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return restResponse({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserInfo(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserDetailsSerializer
    model = UserDetails

    def get_queryset(self):
        queryset = UserDetails.objects.filter(user=self.request.user)
        return queryset


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_categories_info(request):
    queryset = Categories.objects.filter(isActive=True)
    serializer = CategoriesSerializer(queryset, many=True)
    print(serializer.data)
    return restResponse({"msg": "Categories Info", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes(AUTHENTICATION_CLASSES)
@permission_classes([permissions.IsAuthenticated])
@parser_classes([JSONParser])
def create_service_request(request):
    request.data['user_id'] = request.user.id
    serializer = ServiceRequestNewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return restResponse({"msg": "Request created successfully"}, status=status.HTTP_200_OK)
    else:
        error_string = error_message_handler(serializer.errors)
        if error_string:
            return restResponse({"msg": error_string}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return restResponse({"msg": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes(AUTHENTICATION_CLASSES)
@permission_classes([permissions.IsAuthenticated])
@parser_classes([JSONParser])
def get_submitted_requests(request):
    query_set = ServiceRequest.objects.filter(user=request.user.id).order_by('-created')
    main_dict = {"Pending": query_set.filter(status='Pending'), "Completed": query_set.filter(status='Completed')}

    result_dict = {}
    for key, value in main_dict.items():
        date_distinct_list = value.values('created').distinct()
        ind_date_data_list = []
        for date_list_ind in date_distinct_list:
            data_dict = {'Date': date_list_ind['created']}
            ind_date_list = value.filter(created=date_list_ind['created'])
            serializer = ServiceRequestNewSerializer(ind_date_list, many=True)
            data_dict["Requests"] = serializer.data
            ind_date_data_list.append(data_dict)
        result_dict[key] = ind_date_data_list

    return restResponse({"msg": "Request created successfully", "data": result_dict}, status=status.HTTP_200_OK)

# class CreateUserView(CreateAPIView):
#     model = get_user_model()
#     permission_classes = [s
#         permissions.AllowAny
#     ]
#     parser_classes = [
#         JSONParser
#     ]
#     serializer_class = RegisterSerializer
