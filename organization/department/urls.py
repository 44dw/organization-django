from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'departments'
urlpatterns = [
    path('departments', views.DepartmentList.as_view()),
    path('departments/<int:pk>', views.DepartmentDetails.as_view()),
    path('departments/<int:pk>/rename', views.RenameDepartment.as_view()),
    path('departments/<int:pk>/subordinate', views.SubordinateList.as_view()),
    path('departments/<int:pk>/move/<int:parent_department_id>', views.MoveDepartment.as_view()),
    path('departments/<int:pk>/upper', views.UpperList.as_view()),
    path('departments/<int:pk>/salary', views.DepartmentSalary.as_view()),
    path('departments/name/<name>', views.DepartmentByName.as_view()),
    path('salaries', views.DepartmentSalaries.as_view()),
    path('salaries/<int:pk>', views.DepartmentSalaryDetails.as_view())
]

# allow add to url suffixes like .json
urlpatterns = format_suffix_patterns(urlpatterns)