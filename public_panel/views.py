from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views import View
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.utils.safestring import mark_safe
from blogs.models import Blog, BlogPage
from services.models import Service, ServicePage, ServiceImage
from mainapp.models import HomeBanner


class IndexPageView(View):
    template_name = "public_panel/index.html"

    def get(self, request: Any) -> Any:
        service = Service.objects.order_by("priority").prefetch_related("images").all()
        service_page = ServicePage.objects.first() or None
        home_banner = HomeBanner.objects.first() or None

        context = {
            "services": service,
            "service_page": service_page,
            "home_banner": home_banner,
        }
        return render(request, self.template_name, context)


class ServicePageView(View):
    template_name = "public_panel/service.html"

    def get(self, request) -> Any:
        service = Service.objects.order_by("priority").prefetch_related("images").all()
        service_page = ServicePage.objects.first() or None
        context = {
            "services": service,
            "service_page": service_page,
        }
        return render(request, self.template_name, context)


class ServiceDetailPageView(DetailView):
    model = Service
    template_name = "public_panel/service-detail.html"
    context_object_name = "service"

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)
        services = Service.objects.filter(publish=True).exclude(
            id=self.get_object().id
        )[:3]
        if self.object.tags:
            self.object.tag = self.object.tags.split("/")
        data["services"] = services
        return data


class BlogPageView(View):
    template_name = "public_panel/blog.html"

    def get(self, request) -> Any:
        service = Blog.objects.order_by("priority").prefetch_related("images").all()
        service_page = BlogPage.objects.first() or None
        context = {
            "blogs": service,
            "blog_page": service_page,
        }
        return render(request, self.template_name, context)


class BlogDetailPageView(DetailView):
    model = Blog
    template_name = "public_panel/blog-detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)
        services = Blog.objects.filter(publish=True).exclude(id=self.get_object().id)[
            :3
        ]
        if self.object.tags:
            self.object.tag = self.object.tags.split("/")
        data["blogs"] = services
        return data
