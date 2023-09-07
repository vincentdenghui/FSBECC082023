from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lenders import views


router = DefaultRouter()
router.register(r'lenders', views.LenderViewSet,basename='lender')
urlpatterns = [path('', include(router.urls)),]