import datetime

from django.contrib.sessions import models as smodels


def delete_sessions_for_user(user, session_to_omit=None, **kwargs):
    def get_all_sessions_for_user():
        user_sessions = []
        if kwargs.get("unexpired", None):
            all_sessions = smodels.Session.objects.filter(
                expire_date__gte=datetime.datetime.now()
            )
        elif kwargs.get("expired", None):
            all_sessions = smodels.Session.objects.filter(
                expire_date__lt=datetime.datetime.now() - datetime.timedelta(minutes=60)
            )
        elif kwargs.get("all", None):
            all_sessions = smodels.Session.objects.all()
        else:
            all_sessions = smodels.Session.objects.filter(
                expire_date__lt=datetime.datetime.now() - datetime.timedelta(minutes=60)
            )
        if all_sessions:
            for session in all_sessions:
                session_data = session.get_decoded()
                if session_data.get("_auth_user_id") is not None and user.pk == int(
                        session_data.get("_auth_user_id")
                ):
                    user_sessions.append(session.pk)
        return smodels.Session.objects.filter(pk__in=user_sessions)

    session_list = get_all_sessions_for_user()
    if session_to_omit is not None:
        session_list.exclude(session_key=session_to_omit.session_key)
    session_list.delete()
