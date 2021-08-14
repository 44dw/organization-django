from department.models import Department, SalaryFund
from employee.models import Employee

def calc_salary_fund():

    def get_salary_fund_for_department(department):
        employees = Employee.objects.filter(department_id=department.id)
        return sum(map(lambda e: e.salary, employees))

    def create_salary_funds(departments):
        for d in departments:
            salaries = get_salary_fund_for_department(d)
            SalaryFund(d.id, salaries).save()

    print("calculating salary fund...")
    create_salary_funds(Department.objects.all())