ATM
DEPOSIT AND WITHDRAW DJANGO

Installation

Create Environment and Install requirement from requirements.txt.

activate environment and `python manage.py makemigrations && python manange.py migrate`

`python manage.py runserver`

Functionality of the Project is

* 1.Withdraw amount
* 2.deposit amount

Copy the JSON from Postman Collection and export it into **POSTMAN**


Steps to Follow in APIS:

1. **POST** transaction/v1/card/

   this api take 2 input one is for atm code and another one is atm card and this will give card token in response


2. **GET** transaction/v1/card/withdraw/

   this api will create basic withdraw transaction it contains card token in headers


3. **GET** transaction/v1/card/deposit/

   this api will create basic deposit transaction it contains card token in headers


4. **PATCH** transaction/v1/:transactionId/

   in this api it will take 2 argument in body

   one is for amount which we want to make transaction of

   another one is for only deposited transaction that we will send which notes we are sending for deposit

   it will be in body in form of

   `{
   "amount": 1000,
   "in_cash_depo": {
   "500":2
   }`
   }

5. **POST** transaction/v1/:transactionId/verify/

   this is last api of transaction cycle it will just verify a pin of your atm it has card token which should be validated token in header

   after this api you have to re-enter the card and card token will be deleted


there is db.sqlite3 database

superuser credentials:

   username: '**thenils**'
   
   password: '**?**'

