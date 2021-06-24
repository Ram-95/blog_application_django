from .models import Notification


def notifications_exist(request):
    if request.user.is_authenticated:
        f = len(Notification.objects.get_notification_count(request.user))
        status = True if f > 0 else False
        return {
            'status': status,
            'notif_count': f,
        }
    else:
        status = False

    return {'status': status}
