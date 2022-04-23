# Organizations-Django
## What is it?
Sample backend REST service, representing Organization structure, written in Python + Django.
## How to run it?
### Prepare the database
Application expects database in PostgreSQL with next params:
```
{
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'organization',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '',
    'PORT': '5432',
}
```
Modify settings.py if needed
#### Prepare migrations
```shell
python manage.py makemigrations
python manage.py migrate
```
### Start application server
```shell
python manage.py runserver
```
application server will be available on the http://localhost:8000 
### What are the endpoints
#### Departments
Represents **department** in the organization structure  
Example model are the following:  
```json
{
    "id": 1,
    "department_leader": {
        "id": 2,
        "name": "Vasya",
        "surname": "Pupkin",
        "middle_name": "Ivanych",
        "birth_date": "1998-10-25",
        "phone_number": "79379999955",
        "email": "test@mail.com",
        "employment_date": "2020-10-25",
        "dismissal_date": null,
        "position": "engineer",
        "salary": 8885541,
        "is_leader": true,
        "department": 1
    },
    "employees_amount": 2,
    "name": "Development",
    "creation_date": "2021-07-14",
    "parent_department": 3
}
```
**Endpoints**  
**GET /departments** - return the departments list  
**GET /departments/{int:pk}** - return the department by primary key  
**PUT /departments/{int:pk}/rename?name={new_name}** - rename department  
**GET /departments/{int:pk}/subordinate** - get subordinate departments  
**PUT /departments/{int:pk}/move/{int:parent_department_id}** - move department to another parent department  
**GET /departments/{int:pk}/upper** - get all upper departments hierarchy  
**GET /departments/{int:pk}/salary** - get employees salary in particular department  
**GET /departments/name/{name}** - find departments by name
**POST /departments** - add new department with the next request body:
```json
{
    "name": "Development",
    "parent_department": 3
}
```
**DELETE /departments/{int:pk}** - delete department by id  

#### Salaries  
Cumulative **salary** statistic by department  
```json
{
    "department": 1,
    "salary": 8885741
}
```
**GET /salaries** - get all salaries
**GET /salaries/{int:pk}** - get salary object by id

#### Employees
Represents **employee** in the organization  
```json
{
    "id": 8,
    "name": "Dima",
    "surname": "Ivanov",
    "middle_name": "Ivanovich",
    "birth_date": "1991-10-25",
    "phone_number": "79379954854",
    "email": "test@mail.com",
    "employment_date": "2021-08-12",
    "dismissal_date": null,
    "position": "engineer",
    "salary": 200,
    "is_leader": false,
    "department": 1
}
```

**GET /employees** - get all employees  
**GET /employees/{int:pk}** - get employee by id  
**PUT /employees/{int:pk}/dismiss?date={dismissal_date}** - dismiss employee  
**PUT /employees/{int:pk}/move/{int:department_id}** - move employee to another department  
**GET /employees/{int:pk}/supervisor** - get employee supervisor  
**GET /employees/department/{int:department_id}** - get employees in particular department  
**PUT /employees/department/{int:department_id}/move/{int:new_department_id}** - move all employees in one department to another
**POST /employees** - add new employee with the next request body:
```json
{
    "id": 2,
    "name": "Vasya",
    "surname": "Pupkin",
    "middle_name": "Ivanych",
    "birth_date": "1998-10-25",
    "phone_number": "79379999955",
    "email": "test@mail.com",
    "employment_date": "2020-10-25",
    "position": "engineer",
    "salary": 8885541,
    "is_leader": true,
    "department": 1
}
```
**DELETE /employees/{int:pk}** - delete employee by id  