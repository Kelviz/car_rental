import logging
import requests
import json
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.conf import settings



logger = logging.getLogger(__name__)





class CarViewset(viewsets.ModelViewSet):
     queryset = Car.objects.all()
     serializer_class = CarSerializer
     authentication_classes = []
     cache_key_list = 'car_list'
     cache_key_detail = 'car_detail_{}'


     
     def get_queryset(self):   
                queryset = Car.objects.all()
                model = self.request.query_params.get('model', None)
                make = self.request.query_params.get('make', None)
                year = self.request.query_params.get('year', None)
                fuel_type = self.request.query_params.get('fuel_type', None)
                limit = self.request.query_params.get('limit', 11)

                if model is not None:
                        queryset = queryset.filter(model__icontains=model)
                        print(f"there goes model: {model}")
                if make is not None:
                        queryset = queryset.filter(make__icontains=make)
                        print(f"there goes make: {make}")
                if year is not None:
                        if year == 'all':
                            pass
                        else:
                            queryset = queryset.filter(year=year)
                            print(f"there goes year: {year}")

                if fuel_type is not None:
                        queryset = queryset.filter(fuel_type__icontains=fuel_type)
                        print(f"there goes fuel_type: {fuel_type}")

                print(f'Car limit: {limit}')
                
                if limit:
                    print(f'Car limit: {limit}')
                    try:
                            limit = int(limit)
                            queryset = queryset[:limit]

                    except ValueError:
                            pass
                
                return queryset   
     

     @method_decorator(cache_page(60*15, key_prefix=cache_key_list))
     def list(self, request, *args, **kwargs):
                            
        logger.info(f"Fetching cars, cache key: {self.cache_key_list}")
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            return Response({
            'status': status.HTTP_200_OK,
            'message': 'Cars fetched successfully',
            'data': serializer.data
        })
        
        except Exception as e:
               logger.error(f"Error Fetching Interests {e}")
               return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
          
     @method_decorator(cache_page(60*15, key_prefix=lambda view: view.cache_key_detail.format(view.kwargs.get('pk'))))
     def retrieve(self, request, *args, **kwargs):
        car_id = kwargs.get('pk')
        cache_key = self.cache_key_detail.format(car_id)
        logger.info(f"Fetching car details, cache key: {cache_key}")
        response = super().retrieve(request, *args, **kwargs)
        response.data = { 
                'message': 'Car fetched successfully',
                'data': response.data,
                'status': status.HTTP_200_OK,
                
            }
        return response

              
          

     def create(self, request, *args, **kwargs):
              serializer = self.get_serializer(data=request.data)
              serializer.is_valid(raise_exception=True)
              empty_fields = [field for field, value in request.data.items() if value in [None, '', []]]

              if empty_fields:
                        logger.error(f"Empty fields found")
                        error_message = f"Empty fields found: {', '.join(empty_fields)}"
                        logger.error(error_message)
                        return Response({"error": error_message, }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
              

              self.perform_create(serializer)
              cache.delete(self.cache_key_list)
              logger.info(f"Invalidated car list cache, key: {self.cache_key_list}")

              response_data = {
                        'status': 'success',
                        'message': 'Car created successfully',
                        'data': {
                                'Car': serializer.data,
                              
                        }
                }

              return Response(response_data, status=status.HTTP_201_CREATED)
     


     def destroy(self, request, *args, **kwargs):
                car_id = kwargs.get('pk')
                car = Car.objects.filter(id=car_id).first()
                logger.info(f"Deleting Car : {car}")

                if not car:
                    logger.info(f"Car not found")
                    return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
                
                try:
                        super().destroy(request, *args, **kwargs)
                        cache.delete(self.cache_key_list)
                        cache.delete(self.cache_key_detail.format(car_id))
                        logger.info(f"Invalidated car detail cache, key: {self.cache_key_detail.format(car_id)}")
                        return Response({"success": "Car Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
                except Exception as e:
                        logger.error("Error deleting Car: {e}")
                        return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                



     def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        cache.delete(self.cache_key_list)
        cache.delete(self.cache_key_detail.format(instance.pk))
        logger.info(f"Invalidated car detail cache, key: {self.cache_key_detail.format(instance.pk)}")

        response_data = {
            'status': 'success',
            'message': 'Car updated successfully',
            'data': serializer.data
        }

        return Response(response_data)
     
     


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    cache_key_list = 'booking_list'
    cache_key_detail = 'booking_detail_{}'


    @method_decorator(cache_page(60*15, key_prefix=cache_key_list))
    def list(self, request, *args, **kwargs):
        logger.info(f"Fetching bookings, cache key: {self.cache_key_list}")
        try:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                'status': 'success',
                'message': 'Bookings fetched successfully',
                'data': serializer.data
                }, status=status.HTTP_200_OK)
        except Exception as e:
               logger.error(f"Error Fetching Bookings {e}")
               return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @method_decorator(cache_page(60*15, key_prefix=lambda view: view.cache_key_detail.format(view.kwargs.get('pk'))))
    def retrieve(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get('pk')
            cache_key = self.cache_key_detail.format(booking_id)
            logger.info(f"Fetching booking details, cache key: {cache_key}")
            response = super().retrieve(request, *args, **kwargs)
            response.data = {
                'status': 'success',
                'message': 'Booking fetched successfully',
                'data': response.data
            }
            return response
        except Booking.DoesNotExist:
              logger.error(f"Booking doesn't exist")
              return Response({"Not found!": "Booking Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
              


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating New Booking: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empty_fields = [field for field, value in request.data.items() if value in [None, '', []]]

      
        if empty_fields:
                        logger.error(f"Empty fields found")
                        error_message = f"Empty fields found: {', '.join(empty_fields)}"
                        logger.error(error_message)
                        return Response({"error": error_message, }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
        
            self.perform_create(serializer)
            
            cache.delete(self.cache_key_list)
            logger.info(f"Invalidated booking list cache, key: {self.cache_key_list}")
            response_data = {
                'status': 'success',
                'message': 'Booking created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
              logger.error(f"Error Creating Booking {e}")
              return Response({"Error!": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
              
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        cache.delete(self.cache_key_list)
        cache.delete(self.cache_key_detail.format(instance.pk))
        logger.info(f"Invalidated booking detail cache, key: {self.cache_key_detail.format(instance.pk)}")

        response_data = {
            'status': 'success',
            'message': 'Booking updated successfully',
            'data': serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Booking deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    

    @action(detail=False, methods=['get'])
    def current_bookings(self, request):
        user = request.user
        now = timezone.now().date()
        current_bookings = Booking.objects.filter(user=user, end_date__gte=now)
        serializer = self.get_serializer(current_bookings, many=True)
        return Response({
            'status': 'success',
            'message': 'Current bookings fetched successfully',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def expired_bookings(self, request):
        user = request.user
        now = timezone.now().date()
        expired_bookings = Booking.objects.filter(user=user, end_date__lt=now)
        serializer = self.get_serializer(expired_bookings, many=True)
        return Response({
            'status': 'success',
            'message': 'Expired bookings fetched successfully',
            'data': serializer.data
        })
    

class UserView(viewsets.ModelViewSet):
     queryset = UserAccount.objects.all()
     serializer_class = UserSerializer
     permission_classes = [IsAuthenticated]

     def list(self, request, *args, **kwargs):
          logger.info("Fetching Users")
          try:
               queryset = self.get_queryset()
               serializer = self.get_serializer(queryset, many=True)
               return Response({
                    'status': 'success',
                    'message': 'Users fetched successfully',
                    'data': serializer.data      
               }, status=status.HTTP_200_OK)
          
          except Exception as e:
               return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          

     def retrive(self, request, *args, **kwargs):
          try:
               logger.info("Fetching User")
               response = super().retrive(request, *args, **kwargs)
               response.data = {
                    'status': 'success',
                    'message': 'User fetched successfully',
                    'data': response.data,
               }

          except UserAccount.DoesNotExist:
               logger.error("User Does Not Exist")
               return Response({"error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
          
     @action(detail=False, methods=['get'])
     def me(self, request):
          user = request.user
          serializer =self.get_serializer(user)
          logger.info("Fetching Current User Account")
          return Response({
               'status': 'success',
               'message': 'Cureent User Account Fetched Successfully',
               'data': serializer.data
          }, status=status.HTTP_200_OK)


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    
    base_url = 'https://api.paystack.co'

    def verify_payment(self, reference, *args, **kwargs):
        path = f'/transaction/verify/{reference}'
        url = self.base_url + path
        logger.info(f"Verifying payment with Paystack. URL: {url}, Reference: {reference}")
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def initiate_payment(self, email, amount, callback_url):
        path = '/transaction/initialize'
        url = self.base_url + path
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": int(amount * 100),
            "callback_url": callback_url
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()


@csrf_exempt       
def paystack_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = data.get('event')

        if event == 'charge.success':
            payment_data = data.get('data', {})
            reference = payment_data.get('reference')
            amount = payment_data.get('amount') / 100
            status = payment_data.get('status')

            try:
                payment = Payment.objects.get(reference=reference)
                logger.info(f"Found payment: {payment.id} with status {payment.status}")

                if status == 'success':
                            payment.status = 'Completed'
                            payment.save()

                            booking = payment.booking
                            booking.status = 'Confirmed'
                            booking.car.available = False
                            booking.car.save()
                            booking.save()

                            # Delete the cache
                            car_cache_key = f'car_detail_{booking.car.id}'
                            booking_cache_key = f'booking_detail_{booking.id}'

                            cache.delete(car_cache_key)
                            cache.delete(booking_cache_key)
                            logger.info(f"Deleted cache for key: {car_cache_key}") 
                            logger.info(f"Deleted cache for key: {booking_cache_key}") 

                            logger.info(f"Booking {booking.id} status updated to Confirmed")

                            logger.info(f"Receipt generated for payment {payment.id}")

            except Payment.DoesNotExist:
                    logger.error(f"Payment with reference {reference} not found")

            return JsonResponse({"status": "success"}, status=200)


    return JsonResponse({"status": "failed"}, status=400)



class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        paystack = Paystack()
        booking_id = request.data.get('booking_id')
        email = request.data.get('email')
        
        try:
            booking = Booking.objects.get(id=booking_id)
            amount = booking.total_price
            callback_url = 'https://carhuby.vercel.app/callback'
            paystack_response = paystack.initiate_payment(email=email, amount=amount, callback_url = callback_url)

            logger.info(f"Paystack Response: {paystack_response}")
            
            if paystack_response.get('status'):
                payment = Payment.objects.create(
                    booking=booking,
                    amount=amount,
                    status='Pending',
                    reference=paystack_response['data']['reference']
                )
                return Response({
                    "status": "success",
                    "message": paystack_response['message'],
                    "authorization_url": paystack_response['data']['authorization_url']
                }, status=status.HTTP_200_OK)
            
            else:
                error_message = paystack_response.get('message', 'Unknown error')
                logger.error(f"Payment initiation failed: {error_message}")
                return Response({"error": f"Payment initiation failed: {error_message}"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)



class PaystackVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get('reference')
        print(f"ref... {reference}")

        if not reference:
            return JsonResponse({"error": "Reference not provided"}, status=status.HTTP_400_BAD_REQUEST)


        paystack = Paystack()
        verification_response = paystack.verify_payment(reference)
        logger.info(f"Paystack verification response: {verification_response}")

        if verification_response.get('status') == True and verification_response['data'].get('status') == 'success':
            return JsonResponse({"status": "success", "message": "Payment verified successfully"}, status=status.HTTP_200_OK)
        else:
            error_message = verification_response.get('message', 'Verification failed')
            logger.error(f"Payment verification failed: {error_message}")
            return JsonResponse({"status": "failed", "message": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        


