# FSBECC082023

This is my response to the FSBECC082023 coding challenge.
-Vincent W

## Installation

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create a .env file and use the .env_blank as a guide for populating environment variables.
```sh
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DEBUG=
DJANGO_SETTINGS_MODULE=
DJANGO_USER=
DJANGO_USER_PASSWORD=
```
Initialise the database, create the super user and run the app.
```sh
rm -r lenders/migrations
python manage.py makemigrations lenders
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

For production environments:
.env file:
```sh
DEBUG=False
```
and remove all @csrf_exempt decorators:
```sh
@csrf_exempt
```



## Features Implemented
When interacting with the app from a browser user-agent the app shows a human friendly web interface.
Session authentication is used when the user interacts with this API in a browser.
Basic authentication has been implemented for the ease of testing with tools like curl and Postman.


API Usage:

(Example lender 'CBA')

json payload format and limitations:

{
name: str
code: str
upfront_commission_rate: float
trial_commission_rate: float
active: boolean
}

The value constraints of the payload can be found in the LenderFieldConstraints class located in /lenders/models.py.

1. Create a new Lender (login required)
  -POST /lenders/


2. List all Lenders (five per page)
  -GET /lenders/
  -GET /lenders/?page=[1-inf)

3. List active lenders
     -GET /lenders/?active=True (note: only 4 characters input which uppercase is 'TRUE' is deemed True, all other inputs are deemed False)

4. Get a specific Lender 
-GET /lenders/CBA/
-GET /lenders/CBA/?format=api (human friendly)
-GET /lenders/CBA/?format=json (machine friendly)
-GET /lenders/CBA/?format=csv (all friendly)

5. Update a specific Lender (login required)
-PUT /lenders/CBA/

6. Delete a specific Lender (login required)
-DELETE /lenders/CBA/

7. Bulk upload Lenders in CSV format (login required) (this feature is not 100% RESTful)
-POST /csv-in-bulk/ (UTF-8 encoded bytes of a csv with a header)

8. Download Lenders in CSV format (login required) (this feature is not 100% RESTful)
-GET /csv-in-bulk/ (UTF-8 encoded bytes of a csv with a header)

Additional features:
9. List options
-OPTIONS /lenders/ (list the operations supported by this set)

10. Ordering on 'created', 'code', 'upfront_commission_rate', 'trial_commission_rate','active'
-GET /lenders/?ordering=created (ascending order on created)
-GET /lenders/?ordering=-created (descending order on created)
-GET /lenders/?ordering=created,trial_commission_rate (ascending order on created then ascending order on trial_commission_rate)
-GET /lenders/?ordering=created,-trial_commission_rate (ascending order on created then descending order on trial_commission_rate)

For more concrete examples, please have a look at the functional_test.py in the root directory.




