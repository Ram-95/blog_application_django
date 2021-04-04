from .models import Notification

def notifications_exist(request):
    if request.user.is_authenticated:
        f = Notification.objects.filter(receiver=request.user).count()
        status = True if f > 0 else False
    else:
        status = False
    return {
        'status': status,
    }
