from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from bills import api

router = routers.DefaultRouter()
router.register(r'api/upload_bills', api.UploadBills, basename='UploadBills')
router.register(r'api/bills', api.BillsViewSet, basename='BillsInfo')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
