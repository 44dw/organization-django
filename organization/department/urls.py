from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'departments'
urlpatterns = [
    path('departments/', views.DepartmentList.as_view()),
    path('departments/<int:pk>/', views.DepartmentDetails.as_view())
]

# allow add to url suffixes like .json
urlpatterns = format_suffix_patterns(urlpatterns)