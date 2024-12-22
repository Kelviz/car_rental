# Car Rental Showcase - Django Backend

This is the **backend API** for the **Car Rental Showcase** platform. It provides endpoints for managing users, cars, bookings, and authentication for the frontend application. The backend is built using **Django** and **Django Rest Framework (DRF)** and is responsible for handling the business logic, data storage, and user authentication.

## Features

- **User Authentication**:
  - Register and login functionalities.
  - Token-based authentication (JWT) for secure access.
- **Car Management**:
  - List available cars with details such as car class, fuel type, transmission, etc.
  - Add, update, and delete car entries (admin only).
- **Booking System**:

  - Users can book available cars.
  - View current and expired bookings.

- **Payment Integration**:
  - Integrated with **Paystack** for handling payments during car booking.

## Tech Stack

- **Framework**: Django, Django Rest Framework
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: JWT (JSON Web Tokens) using `djangorestframework-simplejwt`
- **Payment Gateway**: Paystack (for payments)

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL (for production)
- Virtual environment setup (optional but recommended)

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/car-rental-backend.git
   cd car-rental-backend

   ```

2. **Create and activate a virtual environment**:
   python -m venv venv
   source venv/bin/activate

3. **Install dependencies**:
   pip install -r requirements.txt

4. **Set up environment variables**:
   Create a .env file in the project root directory

5. **Run database migrations**:
   python manage.py migrate

6. **Create a superuser (for accessing the admin dashboard)**:
   python manage.py createsuperuser

7. **Run the development server**:
   python manage.py runserver

## API Endpoints

### Authentication

- `POST /auth/register/`:

  - Register a new user.

- `POST /auth/login/`:

  - Login and get JWT tokens.

- `POST /auth/refresh-token/`:

  - Refresh the access token using the refresh token.

- `POST /auth/check-auth/`:
  - Check if user is authenticated.

### Cars

- `GET /api/v1/cars/`:

  - List all available cars.

- `GET /api/v1/cars/:id/`:

  - Retrieve a single car's details.

- `POST /api/v1/cars/` (Admin only):

  - Create a new car entry.

- `PUT /api/v1/cars/:id/` (Admin only):

  - Update a car's details.

- `DELETE /api/v1/cars/:id/` (Admin only):
  - Delete a car entry.

### Bookings

- `GET /api/v1/bookings/`:

  - List all bookings

- `GET /api/v1/bookings/current_bookings/`:

  - List all bookings for current user

- `GET /api/v1/bookings/expired_bookings/`:

  - List all expired bookings for current user

- `POST /api/v1/bookings/`:

  - Create a new booking for a car.

- `GET /api/v1/bookings/:id/`:

  - Get details of a specific booking.

- `DELETE /api/v1/bookings/:id/`:
  - Cancel a booking.

### Payments

- `POST /api/payment/initiate/`:

  - Initiate a payment for a booking.

- `POST /api/paystack-webhook/`:
  - Handle payment confirmation via Paystack webhook.
