from .models import PasswordResetRequest


def pending_reset_requests(request):

    if request.user.is_authenticated:

        pending = PasswordResetRequest.objects.filter(
            status=PasswordResetRequest.PENDING
        ).count()

    else:

        pending = 0

    return {

        "pending_reset_requests": pending

    }