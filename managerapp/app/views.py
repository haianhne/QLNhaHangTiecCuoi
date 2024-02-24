from django.shortcuts import render
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth import authenticate, login


from .models import Venue, Service, Menu, FoodItem, Feedback, Order
from .serializers import VenueSerializer, ServiceSerializer, MenuSerializer, \
    FoodItemSerializer, FeedbackSerializer, OrderSerializer


class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)


class ProtectedResourceExampleView(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Protected resource accessed'})


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        from_email = 'your@example.com'  # Update with your email
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
# Create your views here.
