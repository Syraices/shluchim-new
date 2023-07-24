from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("plans.urls")),
    path("plans/", include("plans.urls"), name="plans_list"),
    path("emails/", include("emails.urls")),
    path("my-account/", include("accounts.urls")),
    path("subscribe/", include("subscriptions.urls")),
    path("pages/", include("pages.urls")),
    path('cart/', include("cart.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
