from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'departments'
urlpatterns = [
    path('departments/', views.DepartmentList.as_view()),
    path('departments/<int:pk>/', views.DepartmentDetails.as_view()),
    path('departments/rename/<int:department_id>', views.RenameDepartment.as_view()),
    path('departments/subordinate/<int:department_id>', views.SubordinateList.as_view()),
    path('departments/move/<int:department_id>/<int:parent_department_id>', views.MoveDepartment.as_view()),
    path('departments/upper/<int:department_id>/', views.UpperList.as_view()),
    path('departments/name/<name>/', views.DepartmentByName.as_view()),
    path('departments/salary/<int:department_id>/', views.DepartmentSalary.as_view()),
    path('salaries/', views.DepartmentSalaries.as_view()),
    path('salaries/<int:pk>/', views.DepartmentSalaryDetails.as_view())
]

# allow add to url suffixes like .json
urlpatterns = format_suffix_patterns(urlpatterns)