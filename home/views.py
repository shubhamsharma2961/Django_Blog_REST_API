from rest_framework.views import APIView
from rest_framework.response import Response
from home.serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import traceback
from home.models import Blog
from django.db.models import Q
from home.pagination import CustomPagination
from account.permissions import IsAdminUser

class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            #page_number = request.GET.get('page', 1)
            #paginator = Paginator(blogs, 1)
            #serializer = BlogSerializer(paginator.page(page_number), many= True)
            paginator = CustomPagination()
            paginated_blogs = paginator.paginate_queryset(blogs, request)
            serializer = BlogSerializer(paginated_blogs, many=True)

            return paginator.get_paginated_response(serializer.data)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'    
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            traceback.print_exc()
            print (e)
            return Response({
                'data': {},
                'message':'something went wrong or invalid page'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user= request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search)|Q(blog_text__icontains = search))
            
            paginator = CustomPagination()
            paginated_blogs = paginator.paginate_queryset(blogs, request)
            serializer = BlogSerializer(paginated_blogs, many=True)

            return paginator.get_paginated_response(serializer.data)

            serializer= BlogSerializer(blogs, many= True)
            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'    
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            traceback.print_exc()
            print (e)
            return Response({
                'data': {},
                'message':'something went wrong from this side'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            #print('######')
            #print(request.user)
            #print('######')
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message': 'something went wrong'
                }, status= status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog post sucessfully created'    
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            traceback.print_exc()
            print (e)
            return Response({
                'data': {},
                'message':'something went wrong from this side'
                }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'),user= request.user)

            if not blog.exists():
                return Response({
                'data': {},
                'message':'Blog not found or you are not authorized to edit this blog'
                }, status=status.HTTP_400_BAD_REQUEST)
           
            serializer= BlogSerializer(blog.first(), data = data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message': 'Validdation failed'
                }, status= status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog post updated successfully'    
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            traceback.print_exc()
            print (e)
            return Response({
                'data': {},
                'message':'something went wrong from this side'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
    def delete(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = request.data.get('uid'), user=request.user)

            if not blog.exists():
                return Response({
                'data': {},
                'message':'Blog not found or you are not authorized to delete this blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            blog.first().delete()

            return Response({
                'data':{},
                'message': 'blog post successfully deleted'
                },status=status.HTTP_200_OK)
        
        except Exception as e:
            traceback.print_exc()
            print(e)

            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)


class BlogAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Blogs fetched successfully'
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Blog created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors,
            'message': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Blog updated successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'data': serializer.errors,
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response({
                'message': 'Blog not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            blog.delete()
            return Response({
                'message': 'Blog deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Blog.DoesNotExist:
            return Response({
                'message': 'Blog not found'
            }, status=status.HTTP_404_NOT_FOUND)