from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect


class AdminLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    # check for user login not admin

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_user,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def redirect_if_logged_in(redirect_to="/"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_anonymous:
                return HttpResponseRedirect(redirect_to)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
