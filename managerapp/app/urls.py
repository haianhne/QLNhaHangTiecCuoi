from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('venue', views.VenueViewSet)
router.register('service', views.ServiceViewSet)
router.register('menu', views.MenuViewSet)
router.register('fooditem', views.FoodItemViewSet)
router.register('feedback', views.FeedbackViewSet)
router.register('order', views.OrderViewSet)
router.register('user', views.UserViewset)

urlpatterns = [
    path('', include(router.urls)),
]
