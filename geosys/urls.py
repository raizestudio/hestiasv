from django.urls import path
from rest_framework.routers import DefaultRouter

from geosys.views import (
    AddressViewSet,
    CityTypeViewSet,
    CityViewSet,
    ContinentViewSet,
    CountryViewSet,
    DepartmentViewSet,
    RegionViewSet,
    StreetLabelViewSet,
    StreetViewSet,
)

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="addresses")
router.register("continents", ContinentViewSet, basename="continents")
router.register("countries", CountryViewSet, basename="countries")
router.register("regions", RegionViewSet, basename="regions")
router.register("departments", DepartmentViewSet, basename="departments")
router.register("city-types", CityTypeViewSet, basename="city-types")
router.register("cities", CityViewSet, basename="cities")
router.register("street-labels", StreetLabelViewSet, basename="street-labels")
router.register("streets", StreetViewSet, basename="streets")


urlpatterns = router.urls

urlpatterns += []
