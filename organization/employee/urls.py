from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'employees'
urlpatterns = [
    path('employees', views.EmployeeList.as_view()),
    path('employees/<int:pk>', views.EmployeeDetails.as_view()),
    path('employees/<int:pk>/dismiss', views.Dismiss.as_view()),
    path('employees/<int:pk>/move/<int:department_id>', views.MoveToDepartment.as_view()),
    path('employees/<int:pk>/supervisor', views.EmployeeSupervisor.as_view()),
    path('employees/department/<int:department_id>', views.DepartmentEmployees.as_view()),
    path('employees/department/<int:department_id>/move/<int:new_department_id>', views.MoveAllToDepartment.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)