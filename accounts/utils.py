def login_redirect(user):

    if user.role == "ADMIN":
        return "dashboard:home"

    if user.role == "TREASURER":
        return "dashboard:home"

    return "dashboard:home"