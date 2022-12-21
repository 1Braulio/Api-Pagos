from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'payments', api.PaymentUserViewSet, 'payment_user')

api_urlpatterns = router.urls