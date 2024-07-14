from django import forms
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django_svg_image_form_field import SvgAndImageFormField
from utils.permissions import AdminLoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from mainapp.models import SiteSettings, HomeBanner
from django.contrib import messages


class LoginPage(LoginView):
    template_name = "admin_panel/login.html"
    redirect_authenticated_user = True


class AdminIndex(AdminLoginRequiredMixin, generic.TemplateView):
    template_name = "admin_panel/index.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        return data


@login_required
def logoutFunc(request):
    logout(request)
    return redirect(reverse_lazy("login"), permanent=True)


class SitesettingView(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = SiteSettings
    fields = "__all__"

    def get_object(self, queryset=None):
        obj = SiteSettings.objects.first() or None
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Site Settings"

        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["location_iframe"].widget = forms.Textarea(attrs={"rows": 2})
        return form

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        files = request.FILES
        obj = self.get_object()

        logo = files.get("logo", obj.logo if obj else None)
        print(logo)
        ndata = {
            "phone": data.get("phone", ""),
            "company_email": data.get("company_email", ""),
            "facebook": data.get("facebook", ""),
            "instagram": data.get("instagram", ""),
            "linkedin": data.get("linkedin", ""),
            "address": data.get("address", ""),
            "logo_alt": data.get("logo_alt", ""),
            "location_iframe": data.get("location_iframe", ""),
        }

        if logo:
            if not obj:
                obj = SiteSettings(**ndata)
        obj.logo = logo  # Assign the new logo
        obj.save()  # Save the object after updating the logo

        if not obj:
            SiteSettings.objects.create(**ndata)

            messages.success(request, "Created Successfully!")
        else:
            SiteSettings.objects.all().update(**ndata)
            messages.success(request, "Updated Successfully!")

        return redirect(reverse_lazy("admin_ss"))


class HomeBanners(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = HomeBanner
    fields = "__all__"

    def get_object(self, queryset=None):
        obj = HomeBanner.objects.first() or None
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Home Banner"

        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["image"] = SvgAndImageFormField()
        form.fields["background_image"] = SvgAndImageFormField()

        return form

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        files = request.FILES
        obj = self.get_object()

        background_image = files.get(
            "background_image", obj.background_image if obj else None
        )
        image = files.get("image", obj.image if obj else None)
        ndata = {
            "title": data.get("title", ""),
            "sub_title": data.get("sub_title", ""),
            "bg_image_alt": data.get("bg_image_alt", ""),
            "alt": data.get("alt", ""),
        }

        if background_image or image:
            if not obj:
                obj = HomeBanner.objects.create(**ndata)
                if background_image:
                    obj.background_image = background_image
                if image:
                    obj.image = image
                obj.save()
                messages.success(request, "Created Successfully!")
            else:
                if background_image:
                    obj.background_image = background_image
                if image:
                    obj.image = image
                obj.save()
                HomeBanner.objects.all().update(**ndata)
                messages.success(request, "Updated Successfully!")

        return redirect(reverse_lazy("admin_hb"))
