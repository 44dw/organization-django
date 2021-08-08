from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'employees'
urlpatterns = [
    path('employees/', views.EmployeeList.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetails.as_view()),
    path('employees/department/<int:department_id>/', views.DepartmentEmployees.as_view()),
    path('employees/dismiss/<int:pk>/', views.Dismiss.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)