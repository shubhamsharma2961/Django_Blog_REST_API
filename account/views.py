from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminUser
from .models import UserProfile
import traceback
from django.db.models import Q

class RegisterView(APIView):

    def post(self, request): 
        try:
            data = request.data
            serializer = RegisterSerializer(data= data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors, 
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data':{},
                'message':'your account is created'
            }, status= status.HTTP_201_CREATED) 

        except Exception as e:
            print(e)
            return Response({
                    'data':(), 
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)

class loginView(APIView):
    def post(self, request):

        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors, 
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            response = serializer.get_jwt_token(data)

            return Response(response,status= status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response({
                'data': {}, 
                'message':'something went wrong',
            }, status = status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response({
                'data': serializer.data,
                'message': 'User profile retrieved successfully'
            }, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'data': {},
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Profile updated successfully'
                }, status=status.HTTP_200_OK)

            return Response({
                'data': serializer.errors,
                'message': 'Validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({
                'data': {},
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.user.delete()
            profile.delete()

            return Response({
                'data': {},
                'message': 'Profile deleted successfully'
            }, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'data': {},
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileFilterSearchView(APIView):
    def get(self, request):
        try:
            query = request.GET.get('query', '')
            #date_of_birth = request.GET.get('date_of_birth', '')
            start_date= request.GET.get('start_date','')
            end_date= request.GET.get('end_date','')

            filters = Q()
            if query:
                filters &= Q(first_name__icontains=query) | Q(number__icontains=query)
            #if date_of_birth:
            if start_date and end_date:
                filters &= Q(date_of_birth__range=[start_date,end_date])
                #filters &= Q(date_of_birth=date_of_birth)

            profiles = UserProfile.objects.filter(filters)

            if not profiles.exists():
                return Response({
                    'data': [],
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UserProfileSerializer(profiles, many=True)
            return Response({
                'data': serializer.data,
                'message': 'User profiles fetched successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserCRUDView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response({
            'data': serializer.data,
            'message': 'User data fetched successfully'
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            data=serializer.save()
            
            return Response({
                'data': data.username,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors,
            'message': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'User updated successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'data': serializer.errors,
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
            user.delete()
            return Response({
                'message': 'User deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class CurrentUserPofileView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get (self,request):
        try:
            profile= UserProfile.objects.get(user=request.user)
            serializer= UserProfileSerializer(profile)
            return Response({
                'data':serializer.data,
                'message':'currently authenticated user profile fetched successfully'
            },status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'data':{},
                'message':'profile does not exist'
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


