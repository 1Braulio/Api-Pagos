from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pagos', api.PagosViewSetCustom, 'pagosCustom')

api_urlpatterns = router.urls