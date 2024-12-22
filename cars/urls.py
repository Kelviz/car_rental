from django.urls import path, include
from rest_framework import routers
from .views import CarViewset, BookingViewSet, InitiatePaymentView, UserView, paystack_webhook, PaystackVerifyView

router = routers.DefaultRouter()



router.register('cars', CarViewset,
                basename="cars")

router.register('bookings', BookingViewSet,
                basename="bookings")


router.register('users', UserView,
                basename="users")



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/payment/initiate/', InitiatePaymentView.as_view(), name='payment'),
    path('api/payment/verify/', PaystackVerifyView.as_view(), name='verify'),
    path('api/paystack-webhook/', paystack_webhook, name='paystack-webhook'),
]