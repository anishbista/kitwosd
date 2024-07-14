from django.urls import path
from public_panel.views import (
    IndexPageView,
    ServicePageView,
    ServiceDetailPageView,
    BlogPageView,
    BlogDetailPageView,
)

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("service/", ServicePageView.as_view(), name="service_page"),
    path(
        "service-detail/<str:slug>",
        ServiceDetailPageView.as_view(),
        name="service_detail",
    ),
    path("blog/", BlogPageView.as_view(), name="blog_page"),
    path(
        "blog-detail/<str:slug>",
        BlogDetailPageView.as_view(),
        name="blog_detail",
    ),
]
