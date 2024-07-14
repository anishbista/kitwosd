from django.views import generic
from services.models import Service, ServiceImage, ServicePage
from django.urls import reverse_lazy
from tinymce.widgets import TinyMCE
from utils.permissions import AdminLoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django import forms
from django_svg_image_form_field import SvgAndImageFormField


class ServicePageContentView(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = ServicePage
    fields = "__all__"

    def get_object(self, queryset=None):
        obj = ServicePage.objects.first() or None
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Service Page"
        return data

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        obj = self.get_object()
        ndata = {
            "title": data.get("title", ""),
            "sub_title": data.get("sub_title", ""),
            "home_description": data.get("home_description", ""),
        }
        if not obj:
            ServicePage.objects.create(**ndata)
            messages.success(request, "Created Successfully!")
        else:
            for key, value in ndata.items():
                setattr(obj, key, value)
            obj.save()
            messages.success(request, "Updated Successfully!")

        return redirect(reverse_lazy("admin_services"))


class ServiceListView(AdminLoginRequiredMixin, generic.ListView):
    queryset = Service.objects.all()
    template_name = "admin_panel/pages/service.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "All Services"
        return data


class ServiceCreateView(AdminLoginRequiredMixin, generic.CreateView):
    queryset = Service.objects.all()
    template_name = "admin_panel/forms/create-form-only.html"

    fields = [
        "meta_title",
        "meta_description",
        "title",
        "slug",
        "short_description",
        "description",
        "logo",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("admin_service_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["short_description"].widget = forms.Textarea(attrs={"rows": 4})
        form.fields["tags1"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags2"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags3"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags4"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags5"] = forms.CharField(max_length=1000, required=False)
        form.fields["description"].widget = TinyMCE()
        form.fields["logo"] = SvgAndImageFormField()

        return form

    def form_valid(self, form):
        print("anish", form.cleaned_data["logo"])
        self.object = form.save(commit=False)
        tags = [form.cleaned_data[f"tags{i}"] for i in range(1, 6)]
        self.object.tags = " / ".join(tags)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Create New Service"
        return data


class ServiceUpdateView(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = Service

    fields = [
        "meta_title",
        "meta_description",
        "title",
        "slug",
        "short_description",
        "description",
        "logo",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("admin_service_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["short_description"].widget = forms.Textarea(attrs={"rows": 4})
        form.fields["tags1"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags2"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags3"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags4"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags5"] = forms.CharField(max_length=1000, required=False)
        form.fields["description"].widget = TinyMCE()
        form.fields["logo"] = SvgAndImageFormField()

        return form

    def get_initial(self):
        initial = super().get_initial()

        tags = self.object.tags.split(" / ")
        for i, feature in enumerate(tags, 1):
            initial[f"tags{i}"] = feature
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        tags = [form.cleaned_data[f"tags{i}"] for i in range(1, 6)]
        self.object.tags = " / ".join(tags)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Update Service"

        return data


class ServiceDeleteView(AdminLoginRequiredMixin, generic.DeleteView):
    queryset = Service.objects.all()
    template_name = "admin_panel/forms/create-form-only.html"

    def get_success_url(self):
        return reverse_lazy("admin_service_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Delete Service ?"

        return data


class ServiceImageListView(generic.ListView):
    template_name = "admin_panel/pages/service_images.html"

    paginate_by = 10

    def get_queryset(self):
        service = get_object_or_404(Service, id=self.kwargs["pk"])
        queryset = ServiceImage.objects.filter(service=service)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "All Images"
        data["id"] = self.kwargs["pk"]
        return data


class ServiceImageCreateView(generic.CreateView):
    model = ServiceImage
    template_name = "admin_panel/forms/create-form-only.html"
    fields = [
        "name",
        "image",
        "alt",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        service_id = self.kwargs["pk"]
        return reverse_lazy("admin_service_image_list", kwargs={"pk": service_id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Add New Image"
        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["image"] = SvgAndImageFormField()

        return form

    def form_valid(self, form):
        service_slug = self.kwargs["pk"]
        service = get_object_or_404(Service, id=service_slug)
        form.instance.service = service
        return super().form_valid(form)


class ServiceImageUpdateView(generic.UpdateView):
    model = ServiceImage
    template_name = "admin_panel/forms/create-form-only.html"
    fields = [
        "name",
        "image",
        "alt",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        service_id = self.kwargs["pk"]
        return reverse_lazy(
            "admin_service_image_list", kwargs={"pk": self.object.service.id}
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["image"] = SvgAndImageFormField()

        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Update Image"

        return data


class ServiceImageDeleteView(generic.DeleteView):
    model = ServiceImage
    template_name = "admin_panel/forms/create-form-only.html"

    def get_success_url(self) -> str:
        service_id = self.kwargs["pk"]
        return reverse_lazy(
            "admin_service_image_list", kwargs={"pk": self.object.service.id}
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Delete Image ?"

        return data
