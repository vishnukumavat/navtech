# Introduction

Thes project implements the basic features of inventory/order management system.

It supports the following features served via REST endpoint. 



User
- Register
- User Login/Logout
- Get User Profile
- Place Order

Admin
- Admin Dashboard 
- Create/Update Product (Admin Only)
- Get Order Statistics

The application is hosted live on heroku for demo -

```REST``` - https://navtech.herokuapp.com/test/ 

```Admin Panel``` - https://navtech.herokuapp.com/admin/

(credentials for admin dashboard will be shared via email)

ALl the REST endpoints mentioned can be found as postman collection with all the environment variables configured 

```Postman Collection``` - https://www.getpostman.com/collections/c81dd00f69806a540202


NOTE - A third party library [Djoser](https://djoser.readthedocs.io/) has been used to accomodate ```VIEWS``` for user authentication.

# Getting Started

## Installation
Clone the repository by the following command
```sh
$ git clone https://github.com/vishnukumavat/navtech.git
```

change the current directory to navtech
```sh
$ cd navtech
```

Install all the requirements

```sh
$ pip3 install -r requirements.txt
```

Migrate the data base
```sh
$ python3 manage.py migrate
```

And we are good to go, the below command will spin up the local server on port 8000
```sh
$ python3 manage.py runserver
```

The installation can be verified by making a curl request from your terminal 
```sh
$ curl --location --request GET 'http://127.0.0.1:8000/test'
{"result":"Success","data_base_connection":true,"message":"Hello from GET request"}

```


# Available Endpoints

### `GET` - `/test/`

Sample Usage
```sh
$ curl --location --request GET 'http://127.0.0.1:8000/test'

response-
{"result":"Success","data_base_connection":true,"message":"Hello from GET request"}

```

### `POST` - `/test/`

Sample Usage
```sh
$ curl --location --request POST 'http://localhost:8000/test/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "post_message": "Hello this message is from the POST request"
}'

response -
{
    "result": "Success",
    "data_base_connection": true,
    "message": "Hello from POST request",
    "request_message": "Hello this message is from the POST request"
}

```


### `POST` - `/auth/users/`

Register New User

Sample Usage
```sh
$ curl --location --request POST 'http://localhost:8000/auth/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "anurag",
    "password": "AnuragKaushal@1999"
}'

response -
STATUS - 201 Created
{
    "email": "",
    "username": "anurag",
    "id": 1
}

STATUS - 400 Bad Request
{
    "username": [
        "A user with that username already exists."
    ]
}

```

### `POST` - `/auth/token/login/`

User Login 

Sample Usage
```sh
$ curl --location --request POST 'http://localhost:8000/auth/token/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "anurag",
    "password": "AnuragKaushal@1999"
}'

response -
STATUS - 200 OK
{
    "auth_token": "dfda1751df83f1fa8d01747ec959cb276c08339d"
}

STATUS - 400 Bad Request
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}

```


### `POST` - `/auth/token/logout/`

User Logout

Sample Usage
```sh
$ curl --location --request POST 'http://localhost:8000/auth/token/logout/' \
--header 'Authorization: Token dfda1751df83f1fa8d01747ec959cb276c08339d'

response -
STATUS - 204 No Content

STATUS - 401 nauthorized
{
    "detail": "Invalid token."
}

```

### `GET` - `/auth/users/me/`

User Profile

Sample Usage
```sh
$ curl --location --request GET 'http://localhost:8000/auth/users/me/' \
--header 'Authorization: Token e13f291be822d843400df23d58beacffd66d4ce8'

response -
STATUS - 200 OK
{
    "email": "",
    "id": 1,
    "username": "anurag"
}

STATUS - 401 nauthorized
{
    "detail": "Invalid token."
}

```

### `POST` - `/create_update_product/`

Create Or Update Product

Sample Usage

```test.csv```
|product_name|available_quantity|price|
| --- | --- | --- |
|grape|89|32|
|apple|12|random|

```sh
$ curl --location --request POST 'http://localhost:8000/create_update_product/' \
--header 'Authorization: Token 1ad105ed6537d66dfeafd1666720bee07799435d' \
--form 'file=@"/path/test.csv"'

response -
STATUS - 200 OK
{
    "rejected_items": [
        {
            "product_name": "apple",
            "available_quantity": "12",
            "price": "random"
        }
    ]
}

STATUS - 403 Forbidded
{
    "detail": "You do not have permission to perform this action."
}

STATUS - 401 nauthorized
{
    "detail": "Invalid token."
}

```

### `GET` - `/order_stats/`

Get Order Statistics

Sample Usage
```sh
$ curl --location --request GET 'http://localhost:8000/order_stats/' \
--header 'Authorization: Token d03c9bea927619650b792c55d3c3b7b59d7d4ca7'

response -
STATUS - 200 OK
{
    "result": "success",
    "total_records": 3,
    "stats": [
        {
            "Product Name": "APPLE",
            "Ordered Quantity": 10,
            "At Price": 22,
            "Total Amount": 220
        },
        {
            "Product Name": "APPLE",
            "Ordered Quantity": 100,
            "At Price": 13,
            "Total Amount": 1300
        },
        {
            "Product Name": "ORANGE",
            "Ordered Quantity": 32,
            "At Price": 7,
            "Total Amount": 224
        }
    ]
}

STATUS - 403 Forbidded
{
    "detail": "You do not have permission to perform this action."
}

STATUS - 401 nauthorized
{
    "detail": "Invalid token."
}

```

### `POST` - `/place_order/`

Place Orders

Sample Usage
```sh
$ curl --location --request POST 'http://localhost:8000/place_order/' \
--header 'Authorization: Token 0e3f7584e539babafd37efef3a6221cdcd5ff79f' \
--header 'Content-Type: application/json' \
--data-raw '{
    "orders": [
        {
            "product_name": "apple",
            "quantity": 20
        },
        {
            "product_name": "orange",
            "quantity": 2
        }
    ]
}'

response -
STATUS - 200 OK
    success -
{
    "result": "success",
    "message": "order placed successfully"
}
    error -
{
    "result": "error",
    "message": "Items unavailable - [{'product_name': 'orange', 'quantity': 2, 'available_quantity': 0}]"
}

STATUS - 401 nauthorized
{
    "detail": "Invalid token."
}

```