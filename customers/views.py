import logging
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import UserAccount
from .serializers import UserCreateSerializer, UserSerializer, LoginSerializer



logger = logging.getLogger(__name__)

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        logger.info("Creating New User")
        serializer = UserCreateSerializer(data=request.data)
        empty_fields = [field for field, value in request.data.items() if value in [None, '', []] and field != 'phone']
        if empty_fields:
                        logger.error(f"Empty fields found {e}")
                        error_message = f"Empty fields found: {', '.join(empty_fields)}"
                        logger.error(error_message)
                        return Response({"error": error_message, }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                logger.info(f"New User: {request.data['first_name']}")

                return Response({
                        'status': 'success',
                        'message': 'Registration successful!',
                        'data': {
                        'accessToken': str(refresh.access_token),
                        'user': UserSerializer(user).data
                        }
                }, status=status.HTTP_201_CREATED)
            
            except IntegrityError as e:
                logger.error(f"Bad Request, Registration unsuccessful {e}")

                return Response({
                    'status': 'Bad request',
                    'message': 'Registration unsuccessful!',
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST) 
        
        logger.error(f"Bad Request, Registration unsuccessful {serializer.errors}")   

        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful!',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
 

class LoginView(APIView):
      authentication_classes = []
      permission_classes = []


      def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            logger.info(f"Attempting to sign user in: {email}")

            try:
                user = UserAccount.objects.get(email=email)
                if not user.check_password(password):
                    logger.warning(f"Invalid password for email: {email}")
                    return Response({"error": "Invalid password email or password"}, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                logger.info(f"User signed in successfully: {user.get_full_name()}")
                return Response({
                        'status': 'success',
                        'message': 'Sign In Successful',
                        'data': {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user': UserSerializer(user).data
                        }
                }, status=status.HTTP_200_OK)

            except UserAccount.DoesNotExist:
                logger.warning(f"User does not exist: {email}")
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.warning("Email and password are required")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'status': 'success',
            'message': 'User is authenticated'
        }, status=status.HTTP_200_OK)



class TokenRefreshView(TokenRefreshView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        logger.info(f"Refresh token received: {request.data.get('refresh_token')}")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            logger.info(f"Access Token Refreshed Successfully")

            return Response({
                'status': 'success',
                'access_token': str(access_token)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

          
     
               
          


     