from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('bills', views.BillViewSet, basename='bills')

bills_router = routers.NestedDefaultRouter(router, 'bills', lookup='bill')
bills_router.register('items', views.BillItemViewSet, basename='bill-items')

urlpatterns = router.urls + bills_router.urls
