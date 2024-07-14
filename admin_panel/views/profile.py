from typing import Any
from django.views import generic
from utils.permissions import AdminLoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from admin_panel.forms.profile import PassowrdChangeForm


class ProfileView(AdminLoginRequiredMixin, generic.TemplateView):
    template_name = "admin_panel/pages/profile.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data["ss"] = SiteSettings.objects.first() or None
        return data


@login_required
def change_password(request: HttpRequest):
    if request.method == "POST":
        user = request.user
        form = PassowrdChangeForm(data=request.POST)

        if not form.is_valid():
            return JsonResponse(
                data={
                    "title": "Password Change",
                    "message": form.errors.get("current") or "Form is not valid",
                    "code": 400,
                },
            )
        else:
            current = form.cleaned_data.get("current")
            new = form.cleaned_data.get("new")
            confirm = form.cleaned_data.get("confirm")
        if not user.check_password(current):
            return JsonResponse(
                data={
                    "title": "Password Change",
                    "message": "Current Password Was Incorrect!",
                    "code": 400,
                },
            )
        if new != confirm:
            return JsonResponse(
                data={
                    "title": "Password Change",
                    "message": "Passwords Did Not Match!",
                    "code": 400,
                }
            )

        if new == current:
            return JsonResponse(
                data={
                    "title": "Password Change",
                    "message": "New password should be other than current password!",
                    "code": 400,
                }
            )
        user.set_password(new)
        user.save()
        return JsonResponse(
            data={
                "title": "Password Change",
                "message": "Password Changed Successfully!",
                "code": 200,
            }
        )
    return JsonResponse(
        data={
            "title": "Password Change",
            "message": "Method Not Allowed!",
            "code": 403,
        }
    )


@login_required
def profile_update(request: HttpRequest):
    if request.method == "POST":
        try:
            user = request.user
            data = request.POST
            for key in data:
                setattr(user, key, data[key])

            user.save()
            return JsonResponse(
                data={
                    "title": "Profile Update",
                    "message": "Profile Updated Successfully!",
                    "code": 200,
                }
            )
        except Exception as e:
            return JsonResponse(
                data={
                    "title": "Profile Update",
                    "message": f"{e.args[0]}",
                    "code": 400,
                }
            )

    return JsonResponse(
        data={
            "title": "Profile Update",
            "message": "Method Not Allowed!",
            "code": 403,
        }
    )
