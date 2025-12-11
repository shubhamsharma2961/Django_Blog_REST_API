from django.urls import path
from home.views import PublicBlog
from home.views import BlogView, BlogAdminView

urlpatterns = [
    path('', PublicBlog.as_view()),
    path('blog/', BlogView.as_view()),
    path('blog-admin/', BlogView.as_view()),
    path('blog-admin/<int:pk>/', BlogAdminView.as_view())
]
