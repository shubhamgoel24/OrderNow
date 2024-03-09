# OrderNow

It is an app based in Django for ordering food from various restaurants. It provides the following functionalities:
- User Registration, updating and deleting account.
- Login

## Setup
Follow these steps to set up and run an existing Django project on your local machine.


1. **Python**: Ensure that Python is installed on your system. You can download the latest version of Python from [python.org](https://www.python.org/downloads/).

2. **Clone the Project Repository**: Clone the repository to your local machine.
```bash
git clone <repository-url>
cd <project-directory>

```

3. **Virtual Environment (Optional but Recommended)**: If the project doesn't already have a virtual environment, you can create one to isolate project dependencies.

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

5. **Install Dependencies**: Install project dependencies using the package manager (usually pip).
```bash
pipenv install
```

6. **Apply Migrations**: Apply any necessary database migrations.
```bash
python manage.py migrate
```

7. **Run the Development Server**: Start the development server.
```bash
python manage.py runserver
```

## Usage

### 1. <BASE_URL>/users/
Method: POST

This endpoint handles user Registration.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request POST '<BASE_URL>/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user5",
    "password": "username@1",
    "email": "user5@test.com",
    "city": "new",
    "state": "delhi",
    "zipcode": "110019",
    "first_name": "Test",
    "last_name": "User"
}'
```

- Response
```json
{
    "status": "success",
    "code": 201,
    "data": {
        "username": "user5",
        "city": "new",
        "state": "delhi",
        "zipcode": "110019",
        "first_name": "Test",
        "last_name": "User",
        "balance": 1000,
        "id": 31,
        "email": "user5@test.com"
    },
    "message": null
}
```

### 2. <BASE_URL>/login/
Method: POST

This endpoint handles user login.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request POST '<BASE_URL>/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user5",
    "password": "username@1"
}'
```

- Response
```json
{
    "status": "success",
    "code": 200,
    "data": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    },
    "message": null
}
```

### 3. <BASE_URL>/token/refresh/
Method: POST

This endpoint is used for getting new json token.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request POST '<BASE_URL>/token/refresh/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}'
```

- Response
```json
{
    "status": "success",
    "code": 200,
    "data": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    },
    "message": null
}
```

### 4. <BASE_URL>/users/
Method: GET

This endpoint is used for fetching details of current logged in user.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request GET '<BASE_URL>/users/' \
--header 'Authorization: Bearer token'
```

- Response
```json
{
    "status": "success",
    "code": 200,
    "data": [
        {
            "username": "user5",
            "city": "new",
            "state": "Delhi8",
            "zipcode": "110019",
            "first_name": "Test",
            "last_name": "User",
            "balance": 1000,
            "id": 24,
            "email": "user5@test.com"
        }
    ],
    "message": null
}
```

### 5. <BASE_URL>/users/<id>/
Method: DELETE

This endpoint is used for deactivating user account.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request DELETE '<BASE_URL>/users/<id>/' \
--header 'Authorization: Bearer token'
```

- Response
```json
{
    "status": "success",
    "code": 204,
    "data": null,
    "message": null
}
```


### 6. <BASE_URL>/users/<id>/
Method: PATCH

This endpoint is used for updating user account details.

**Example**
- Curl for invoking this endpoint
``` curl
curl --location --request PATCH '<BASE_URL>/users/<id>/' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "New"
}'
```

- Response
```json
{
    "status": "success",
    "code": 200,
    "data": {
        "username": "user5",
        "city": "new",
        "state": "Delhi",
        "zipcode": "110019",
        "first_name": "New",
        "last_name": "User",
        "balance": 1000,
        "id": 31,
        "email": "user5@test.com"
    },
    "message": null
}
```
