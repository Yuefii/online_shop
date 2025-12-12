# Online Shop API Specifications

This document outlines the API endpoints, authentication mechanisms, and data schemas for the Online Shop API.

## Base URL

The API is typically served at `http://localhost:8000`.

## Authentication

The API uses OAuth2 with Password Flow (Bearer Token).

- **Login Endpoint**: `/auth/login`
- **Protected Endpoints**: Require `Authorization: Bearer <access_token>` header.
- **Refresh Token**: Used to obtain new access tokens via `/auth/refresh`.

## Rate Limiting

- **Global policy**: Not specified.
- **Specific endpoints**: `/auth/*` endpoints are limited to **5 requests per minute**.

## Error Handling

Standard HTTP status codes are used:

- `200`: Success
- `400`: Bad Request (Validation errors, invalid credentials)
- `401`: Unauthorized (Invalid or expired token)
- `429`: Too Many Requests (Rate limit exceeded)

---

## Endpoints

### 1. Authentication (`/auth`)

#### Register User

Create a new user account.

- **URL**: `/auth/register`
- **Method**: `POST`
- **Rate Limit**: 5/minute
- **Request Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword1",
    "full_name": "John Doe"
  }
  ```
  _Note: Password must be at least 8 characters and contain at least one number._
- **Response**:
  - `200 OK`: `{"message": "User created"}`
  - `400 Bad Request`: Email already registered.

#### Login

Authenticate a user and retrieve access tokens.

- **URL**: `/auth/login`
- **Method**: `POST`
- **Rate Limit**: 5/minute
- **Content-Type**: `application/x-www-form-urlencoded`
- **Request Body**:
  - `username`: Email address
  - `password`: User password
- **Response**:
  - `200 OK`:
    ```json
    {
      "access_token": "eyJhbG...",
      "refresh_token": "eyJhbG...",
      "token_type": "bearer"
    }
    ```
  - `400 Bad Request`: Invalid credentials.

#### Refresh Token

Get a new access token using a valid refresh token.

- **URL**: `/auth/refresh`
- **Method**: `POST`
- **Headers**:
  - `x-refresh-token`: `<your_refresh_token>`
- **Response**:
  - `200 OK`:
    ```json
    {
      "access_token": "new_access_token...",
      "token_type": "bearer"
    }
    ```
  - `401 Unauthorized`: Invalid or expired refresh token.

### 2. Users (`/users`)

#### Get Current User

Retrieve profile information for the currently authenticated user.

- **URL**: `/users/me`
- **Method**: `GET`
- **Authentication**: Required (Bearer Token)
- **Response**:
  - `200 OK`:
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "is_active": true
    }
    ```
