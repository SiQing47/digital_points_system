# **Digital Points System**

This is a simple digital points system designed to manage user points and transaction records.
## **Technology Stack**

- Python
- Django
- Django REST framework

## **Getting Started**

To get started with this project, follow these steps:

1. Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/digital-points-system.git
```
2. Navigate to the project directory.

```bash
cd digital-points-system
```

3. Create a virtual environment and install dependencies.
```bash
python -m venv venv
source venv/bin/activate  # On Windows, it's venv\Scripts\activate.bat
pip install -r requirements.txt
```

4. Start the development server.
```bash
python manage.py runserver
```

The project should now be running at **`http://localhost:8000/`**.


## **API Usage**

This project includes the following API:

- **View User List (with balance):** GET **`/api/users`**
- **View User Detail (with transactions):** GET **`/api/users/<str:id>`**
- **Give Points:** POST **`/api/give-points`**
- **Use Points:** POST **`/api/use-points`**


### User List API

Make a GET request to `/api/users`:

Response:

```json
[
    {
        "id": "4a79a84a-ed7a-4e84-b9ae-2c693772ec10",
        "username": "test_user_001",
        "is_superuser": false,
        "balance": 85
    },
    {
        "id": "733ba7fc-13a5-41f8-aa8c-c45a942f1f64",
        "username": "test_user_002",
        "is_superuser": false,
        "balance": 145
    }
]
```
### User Detail API

This API allows you to look specific user's transactions.

Make a GET request to `/api/users/<str:id>`

Example:
`http://127.0.0.1:8000/api/users/733ba7fc-13a5-41f8-aa8c-c45a942f1f64/`

Response:

```json

{
    "id": "733ba7fc-13a5-41f8-aa8c-c45a942f1f64",
    "username": "test_user_002",
    "is_superuser": false,
    "balance": 145,
    "transactions": [
        {
            "original_balance": 150,
            "source": "CompanyC",
            "transaction_type": "increase",
            "amount": 15,
            "remaining_balance": 165,
            "description": "購物回饋",
            "timestamp": "2023-09-03T06:01:53.005713Z"
        },
        {
            "original_balance": 165,
            "source": "StoreB",
            "transaction_type": "decrease",
            "amount": 20,
            "remaining_balance": 145,
            "description": "折抵購物",
            "timestamp": "2023-09-03T06:13:27.469824Z"
        }
    ]
}
```

### **Points Transaction API**

Description:

This API allows you to perform point transactions, including giving and using points.

Endpoint: 

- **`POST /api/give-points/`**: Perform a points transaction to give points to a user.
- **`POST /api/use-points/`**: Perform a points transaction to use points from a user.

Request Parameters: 

- **`user_id`** (string, required): The unique identifier of the user involved in the transaction.
- **`source`** (string, required): The source of the points (e.g., CompanyA).
- **`amount`** (integer, required): The amount of points involved in the transaction.
- **`description`** (string, required): A description of the transaction.

Example Request:

#### **Giving Points**

```json
{
   "user_id": "4a79a84a-ed7a-4e84-b9ae-2c693772ec10",
   "source": "CompanyA",
   "amount": 50,
   "description": "購物回饋"
}

```

#### **Using Points**

```json
{
   "user_id": "4a79a84a-ed7a-4e84-b9ae-2c693772ec10",
   "source": "StoreB",
   "amount": 20,
   "description": "折抵購物"
}

```

#### Response


- **`original_balance`** (integer): The user's point balance before the transaction.
- **`source`** (string): The source of the points.
- **`transaction_type`** (string): The type of transaction, which can be "increase" or "decrease"
- **`amount`** (integer): The amount of points involved in the transaction.
- **`remaining_balance`** (integer): The type of transaction ('increase' or 'decrease').
- **`description`** (string): The description of the transaction.
- **`timestamp`** (string): The timestamp of the transaction.

#### Example Response

```json
{
    "original_balance": 85,
    "source": "StoreB",
    "transaction_type": "decrease",
    "amount": 50,
    "remaining_balance": 35,
    "description": "兌換贈品",
    "timestamp": "2023-09-03T06:24:26.234905Z"
}

```

### Error Responses

- **400 Bad Request**
  - If the request is missing required parameters or has invalid data.
  - If the transaction type is not 'increase' or 'decrease'.
  - If the user balance is insufficient for a 'decrease' transaction.
- **500 Internal Server Error**: If there is a server error while processing the request.


## Unit Tests
To run unit tests, you can use the following command:
```
python manage.py test
```

