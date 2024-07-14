from django.urls import path
from admin_panel.views import main, profile, services, blogs

urlpatterns = [
    path("", main.AdminIndex.as_view(), name="admin_home"),
    path("login/", main.LoginPage.as_view(), name="login"),
    path("logout/", main.logoutFunc, name="logout"),
    path("profile/", profile.ProfileView.as_view(), name="admin_profile"),
    path("password-change/", profile.change_password, name="admin_pass_ch"),
    path("profile-update/", profile.profile_update, name="admin_profile_ch"),
    path("site-settings/", main.SitesettingView.as_view(), name="admin_ss"),
    path("banners/", main.HomeBanners.as_view(), name="admin_hb"),
    # Service
    path(
        "services/main",
        services.ServicePageContentView.as_view(),
        name="admin_services",
    ),
    path(
        "services/service-items/",
        services.ServiceListView.as_view(),
        name="admin_service_list",
    ),
    path(
        "services/service-item/new/",
        services.ServiceCreateView.as_view(),
        name="admin_service_new",
    ),
    path(
        "services/service-item/<str:pk>/",
        services.ServiceUpdateView.as_view(),
        name="admin_service_edit",
    ),
    path(
        "services/service-item/<str:pk>/delete/",
        services.ServiceDeleteView.as_view(),
        name="admin_service_delete",
    ),
    # Service Image
    path(
        "services/service-item/service-images/<str:pk>/",
        services.ServiceImageListView.as_view(),
        name="admin_service_image_list",
    ),
    path(
        "services/service-item/service-image/new/<str:pk>/",
        services.ServiceImageCreateView.as_view(),
        name="admin_service_image_new",
    ),
    path(
        "services/service-item/service-image/<str:pk>/",
        services.ServiceImageUpdateView.as_view(),
        name="admin_service_image_edit",
    ),
    path(
        "services/service-item/service-image/<str:pk>/delete/",
        services.ServiceImageDeleteView.as_view(),
        name="admin_service_image_delete",
    ),
    # Blog
    path(
        "blogs/main",
        blogs.BLogPageContentView.as_view(),
        name="admin_blogs",
    ),
    path(
        "blogs/blog-items/",
        blogs.BlogListView.as_view(),
        name="admin_blog_list",
    ),
    path(
        "blogs/blog-item/new/",
        blogs.BlogCreateView.as_view(),
        name="admin_blog_new",
    ),
    path(
        "blogs/blog-item/<str:pk>/",
        blogs.BlogUpdateView.as_view(),
        name="admin_blog_edit",
    ),
    path(
        "blogs/blog-item/<str:pk>/delete/",
        blogs.BlogDeleteView.as_view(),
        name="admin_blog_delete",
    ),
    # Blog Image
    path(
        "blogs/blog-item/blog-images/<str:pk>/",
        blogs.BlogImageListView.as_view(),
        name="admin_blog_image_list",
    ),
    path(
        "blogs/blog-item/blog-image/new/<str:pk>/",
        blogs.BlogImageCreateView.as_view(),
        name="admin_blog_image_new",
    ),
    path(
        "blogs/blog-item/blog-image/<str:pk>/",
        blogs.BlogImageUpdateView.as_view(),
        name="admin_blog_image_edit",
    ),
    path(
        "blogs/blog-item/blog-image/<str:pk>/delete/",
        blogs.BlogImageDeleteView.as_view(),
        name="admin_blog_image_delete",
    ),
]
