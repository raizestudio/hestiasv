from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import AppSettingViewSet, MenuViewSet

router = DefaultRouter()
router.register("api/menus", MenuViewSet, basename="menus")
router.register("api/settings", AppSettingViewSet, basename="settings")

urlpatterns = router.urls
urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/users/", include("user.urls")),  # User API
    path("api/authentication/", include("authentication.urls")),  # Authentication API
    path("api/geosys/", include("geosys.urls")),  # Geosys API
    path("api/services/", include("service.urls")),  # Service API
    path("api/assets/", include("asset.urls")),  # Asset API
    path("api/quotations/", include("quotation.urls")),  # Quotation API
    path("api/pros/", include("pro.urls")),  # Pro API
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
