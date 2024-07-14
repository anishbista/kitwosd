from django.views import generic
from blogs.models import Blog, BlogPage, BlogImage
from django.urls import reverse_lazy
from tinymce.widgets import TinyMCE
from utils.permissions import AdminLoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django import forms
from django_svg_image_form_field import SvgAndImageFormField


class BLogPageContentView(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = BlogPage
    fields = "__all__"

    def get_object(self, queryset=None):
        obj = BlogPage.objects.first() or None
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Blog Page"
        return data

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        obj = self.get_object()
        ndata = {
            "title": data.get("title", ""),
            "sub_title": data.get("sub_title", ""),
        }
        if not obj:
            BlogPage.objects.create(**ndata)
            messages.success(request, "Created Successfully!")
        else:
            for key, value in ndata.items():
                setattr(obj, key, value)
            obj.save()
            messages.success(request, "Updated Successfully!")

        return redirect(reverse_lazy("admin_blogs"))


class BlogListView(AdminLoginRequiredMixin, generic.ListView):
    queryset = Blog.objects.all()
    template_name = "admin_panel/pages/blog.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "All Blogs"
        return data


class BlogCreateView(AdminLoginRequiredMixin, generic.CreateView):
    queryset = Blog.objects.all()
    template_name = "admin_panel/forms/create-form-only.html"

    fields = [
        "meta_title",
        "meta_description",
        "title",
        "slug",
        "short_description",
        "description",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("admin_blog_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["short_description"].widget = forms.Textarea(attrs={"rows": 4})
        form.fields["tags1"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags2"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags3"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags4"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags5"] = forms.CharField(max_length=1000, required=False)
        form.fields["description"].widget = TinyMCE()

        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        tags = [form.cleaned_data[f"tags{i}"] for i in range(1, 6)]
        self.object.tags = " / ".join(tags)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Create New Blog"
        return data


class BlogUpdateView(AdminLoginRequiredMixin, generic.UpdateView):
    template_name = "admin_panel/forms/create-form-only.html"
    model = Blog

    fields = [
        "meta_title",
        "meta_description",
        "title",
        "slug",
        "short_description",
        "description",
        "priority",
        "publish",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("admin_blog_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["short_description"].widget = forms.Textarea(attrs={"rows": 4})
        form.fields["tags1"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags2"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags3"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags4"] = forms.CharField(max_length=1000, required=False)
        form.fields["tags5"] = forms.CharField(max_length=1000, required=False)
        form.fields["description"].widget = TinyMCE()

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
        data["title"] = "Update Blog"

        return data


class BlogDeleteView(AdminLoginRequiredMixin, generic.DeleteView):
    queryset = Blog.objects.all()
    template_name = "admin_panel/forms/create-form-only.html"

    def get_success_url(self):
        return reverse_lazy("admin_blog_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Delete Blog ?"

        return data


class BlogImageListView(generic.ListView):
    template_name = "admin_panel/pages/blog_images.html"

    paginate_by = 10

    def get_queryset(self):
        service = get_object_or_404(Blog, id=self.kwargs["pk"])
        queryset = BlogImage.objects.filter(blog=service)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "All Images"
        data["id"] = self.kwargs["pk"]
        return data


class BlogImageCreateView(generic.CreateView):
    model = BlogImage
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
        return reverse_lazy("admin_blog_image_list", kwargs={"pk": service_id})

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
        service = get_object_or_404(Blog, id=service_slug)
        form.instance.blog = service
        return super().form_valid(form)


class BlogImageUpdateView(generic.UpdateView):
    model = BlogImage
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
        return reverse_lazy("admin_blog_image_list", kwargs={"pk": self.object.blog.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["image"] = SvgAndImageFormField()

        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Update Image"

        return data


class BlogImageDeleteView(generic.DeleteView):
    model = BlogImage
    template_name = "admin_panel/forms/create-form-only.html"

    def get_success_url(self) -> str:
        service_id = self.kwargs["pk"]
        return reverse_lazy("admin_blog_image_list", kwargs={"pk": self.object.blog.id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Delete Image ?"

        return data
