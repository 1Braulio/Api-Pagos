from django.urls import re_path, include, path

from pagos.v1.routers import api_urlpatterns as api_v1
from pagos.v2.routers import api_urlpatterns as api_v2

from pagos.v2.api import ServicesView, ExpiredPaymentsView
# from versionedTodo.v4.router import api_urlpatterns as api_v4

# ....

urlpatterns = [
    # ...
    re_path(r'^api/v1/', include(api_v1)),
    re_path(r'^api/v2/', include(api_v2)),
    # re_path(r'^api/v4/', include(api_v4)),
    path('api/v2/pagos/servicios/', ServicesView.as_view(), name = 'servicios_view'),
    path('api/v2/pagos/expired-payments/', ExpiredPaymentsView.as_view(), name = 'expired_payments_view'),

]