# Book Review API

## Overview
This API provides endpoints for managing users, books, and reviews. It includes functionalities for user registration, listing books, adding reviews, and retrieving reviews with detailed user and book information.

## Features
  - **User Registration:** Allows users to register by providing their name, email, and password.
  - **Book Management:** Add, update, and list books with their metadata like title, author, genre, etc.
  - **Review Management:** Users can post reviews for books, and reviews include rating, comment, and timestamps.
  - **JWT Authentication:** Secure the API using JSON Web Tokens (JWT) for user authentication.
  - **Review Readability:** Get reviews with detailed information on both the user who posted the review and the book being reviewed.

## API Endpoints

### 1. POST /register/
  - **Purpose:** Registers a new user with their name, email, and password.
  - **Request Body:**
    ```json
    {
      "name": "John Doe",
      "email": "johndoe@example.com",
      "password": "password123"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "John Doe",
      "email": "johndoe@example.com"
    }
    ```
  - **Common Usage:** User registration for the book review platform.

### 2. POST /token/
  - **Purpose:** Obtain JWT access and refresh tokens for user authentication.
  - **Request Body:**
    ```json
    {
      "email": "johndoe@example.com",
      "password": "password123"
    }
    ```
  - **Response:**
    ```json
    {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
    ```
  - **Common Usage:** Authenticate users and provide them access tokens for further API interactions.

### 3. GET /books/
  - **Purpose:** List all available books in the system.
  - **Response:**
    ```json
    [
      {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Fiction",
        "year_of_publish": 1925,
        "summary": "A story about the Jazz Age in the United States."
      },
      ...
    ]
    ```
  - **Common Usage:** Users can browse books to find what they would like to review.

### 4. POST /books/
  - **Purpose:** Add a new book to the system (Admin only).
  - **Request Body:**
    ```json
    {
      "title": "New Book Title",
      "author": "Author Name",
      "genre": "Fiction",
      "year_of_publish": 2020,
      "summary": "Book description goes here."
    }
    ```
  - **Response:**
    ```json
    {
      "id": 2,
      "title": "New Book Title",
      "author": "Author Name",
      "genre": "Fiction",
      "year_of_publish": 2020,
      "summary": "Book description goes here."
    }
    ```
  - **Common Usage:** Admin users can add new books to the system.

### 5. POST /reviews/
  - **Purpose:** Post a review for a book.
  - **Request Body:**
    ```json
    {
      "book": 1,
      "rating": 5,
      "comment": "An amazing book with deep insights."
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "user": 1,
      "book": 1,
      "rating": 5,
      "comment": "An amazing book with deep insights.",
      "created_at": "2024-10-20T14:35:21.000Z"
    }
    ```
  - **Common Usage:** Users can post reviews for the books they’ve read.

### 6. GET /reviews/
  - **Purpose:** Retrieve all reviews with user and book details.
  - **Response:**
    ```json
    [
      {
        "id": 1,
        "user": "John Doe",
        "book": "The Great Gatsby",
        "rating": 5,
        "comment": "An amazing book with deep insights.",
        "created_at": "2024-10-20T14:35:21.000Z"
      },
      ...
    ]
    ```
  - **Common Usage:** Anyone can browse reviews with detailed information.

## Installation

1. **Clone Repository**: Clone this repository to your local machine.
```bash
git clone https://github.com/yourusername/book_review_api.git
