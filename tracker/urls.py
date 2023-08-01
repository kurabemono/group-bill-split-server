from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('bills', views.BillViewSet, basename='bills')

urlpatterns = router.urls
