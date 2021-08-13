from django_extensions.management.jobs import MinutelyJob
from department.models import Department, SalaryFund
from employee.models import Employee

class Job(MinutelyJob):
    help = "Job to persist salary fund"

    def get_salary_fund_for_department(self, department):
        employees = Employee.objects.filter(department_id=department.id)
        return sum(map(lambda e: e.salary, employees))

    def create_salary_funds(self, departments):
        for d in departments:
            salaries = self.get_salary_fund_for_department(d)
            SalaryFund(d.id, salaries).save()

    def execute(self):
        print("calculating salary fund...")
        self.create_salary_funds(Department.objects.all())
