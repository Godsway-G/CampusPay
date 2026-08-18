from django.contrib.auth.decorators import user_passes_test


def admin_required(view):

    return user_passes_test(

        lambda u: u.is_authenticated and u.role == "ADMIN"

    )(view)


def treasurer_required(view):

    return user_passes_test(

        lambda u: u.is_authenticated and u.role == "TREASURER"

    )(view)


def member_required(view):

    return user_passes_test(

        lambda u: u.is_authenticated and u.role == "MEMBER"

    )(view)