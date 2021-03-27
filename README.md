# Dev Requirements for running locally

## Install required dependencies
* [Install  Python](https://www.python.org/downloads/)
* [Install Mysql](https://dev.mysql.com/downloads/installer/)

## Clone repository & install required packages

```cmd
git clone https://github.com/akjha992/python-flask-mysql-wallet-app.git
cd python-flask-mysql-wallet-app
pip3 install flask
pip3 install flask-mysqldb
pip3 install pyyaml
```

## Create Database in MySQL DB
* Follow [this](https://www.youtube.com/results?search_query=install+mysql+on+windows+10) to setup Mysql locally and setup a password.
* Open MySQL Command Line Client and enter the password.
* Execute the below commands to create required tables.

```mysql
CREATE DATABASE WALLET_TRANSACTION_SYSTEM;

USE WALLET_TRANSACTION_SYSTEM

CREATE TABLE Wallet (
    PhoneNumber varchar(255) NOT NULL PRIMARY KEY,
    Balance double NOT NULL
);

CREATE TABLE Transactions (
    TransactionID int  AUTO_INCREMENT PRIMARY KEY,
    PhoneNumber varchar(255) NOT NULL,
    Amount double,
    FOREIGN KEY (PhoneNumber) REFERENCES Wallet(PhoneNumber)
);
```

## Update db password in codebase
* Open db.yaml in the root directory of the project.
* Replace 'mydbpassword' with the password of your MySQL database.


## Run flask backend server
* Open terminal from the root directory of the project
* Run the below command.

```cmd
python app.py
```
* If everything is correct you will see that the server is hosted locally on http://127.0.0.1:5000/

## Postman Collection Link
   <https://www.getpostman.com/collections/3053f1b2c04347ef8c72>

## API Documentation

### /createNewWallet

* **Description**
 
  Creates a new user wallet entry with a given phone number as a user identifier and the initial balance which must be greater than minimum balance requirement.
Phone number entered should not be linked with any existing user wallet.

* **URL**

  <http://127.0.0.1:5000/createNewWallet>

* **Method:**

   `POST`
  
*  **URL Params**

   None

* **Data Params**

  **Required:**
 
   `phoneNumber=[string]`

   `balance=[double]`

* **Success Response:**

  * **Code:** 200

    **Content:** `Wallet created successfully!`
 
* **Error Response:**

  * **Code:** 400

    **Content:** `Wallet for this user already exists!`

### /getBalance

* **Description**
 
  Fetches the account balance for a given wallet. Account is identified via phone numbers, hence the api takes phone number as a url parameter and returns the available balance in the wallet linked to this user.
This fails if the user does not exist.

* **URL**

  <http://127.0.0.1:5000/getBalance>

* **Method:**

   `GET`
  
*  **URL Params**

   **Required:**

   `phoneNumber=[string]`

* **Data Params**
   
   None

* **Success Response:**

  * **Code:** 200

    **Content:** balance=[double]
 
* **Error Response:**

  * **Code:** 400

    **Content:** `NOT FOUND`

### /debit

* **Description**
 
  Does a debit transaction on the account. Account is identified via phone numbers, hence the api takes phone number as a url parameter and the amount (positive value) to be debited. If there is sufficient balance in the wallet, the amount is debited and new wallet balance is reflected. In any other case the transaction is cancelled.

* **URL**

  <http://127.0.0.1:5000/debit>

* **Method:**

   `GET`
  
*  **URL Params**
  
    None

* **Data Params**

   **Required:**

   `phoneNumber=[string]`

   `balance=[double]`

* **Success Response:**

  * **Code:** 200

    **Content:** `Transaction Successfull!`
 
* **Error Response:**

  * **Code:** 200

    **Content:** `Transaction Failed!!`

### /credit

* **Description**
 
  Does a credit transaction on the account. Account is identified via phone numbers, hence the api takes phone number as a url parameter and the amount (positive value) to be credited. The transaction fails if either the amount is not positive or their is no account linked with the provided phone number.

* **URL**

  <http://127.0.0.1:5000/credit>

* **Method:**

   `GET`
  
*  **URL Params**
  
    None

* **Data Params**

   **Required:**

   `phoneNumber=[string]`

   `balance=[double]`

* **Success Response:**

  * **Code:** 200

    **Content:** `Transaction Successfull!`
 
* **Error Response:**

  * **Code:** 200

    **Content:** `Transaction Failed!!`
