from django.shortcuts import render
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

from . import serializers
from .models import Venue, Service, Menu, FoodItem, Feedback, Order, User
from .serializers import VenueSerializer, ServiceSerializer, MenuSerializer, \
    FoodItemSerializer, FeedbackSerializer, OrderSerializer, UserSerializer


class NoPagination(PageNumberPagination):
    page_size = None


class UserViewset(viewsets.ViewSet, generics.CreateAPIView,
                                    generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NoPagination

    @action(detail=False, methods=['get'])
    def search_wedding_info(self, request):
        venue_id = request.query_params.get('venue_id')
        menu_id = request.query_params.get('menu_id')
        food_item_ids = request.query_params.getlist('food_item_ids')
        service_ids = request.query_params.getlist('service_ids')

        venue = Venue.objects.get(id=venue_id)
        menu = Menu.objects.get(id=menu_id)
        food_items = FoodItem.objects.filter(id__in=food_item_ids)
        services = Service.objects.filter(id__in=service_ids)

        venue_data = VenueSerializer(venue).data
        menu_data = MenuSerializer(menu).data
        food_items_data = FoodItemSerializer(food_items, many=True).data
        services_data = ServiceSerializer(services, many=True).data

        total_amount = venue.price + menu.price + sum(food_item.price for food_item in food_items) + sum(service.price for service in services)

        wedding_info = {
            'venue': venue_data,
            'menu': menu_data,
            'food_items': food_items_data,
            'services': services_data,
            'total_amount': total_amount
        }

        return Response(wedding_info, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def send_order_info(self, request):
        order_data = request.data
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            order_info = serializer.data
            email = request.data.get('email')
            self.send_order_info_email(email, order_info)
            return Response({'message': 'Order information sent successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_order_info_email(self, email, order_info):
        subject = 'Order Information'
        message = f"Thank you for your order. Here's your order information: \n\n {order_info}"
        from_email = 'haianhinclude@gmail.com'  # Update with your email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

