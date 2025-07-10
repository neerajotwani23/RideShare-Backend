# FastAPI Rideshare Backend

A comprehensive rideshare platform backend built with FastAPI, implementing a layered architecture with clean separation of concerns.

## 🚗 Features

### Core Functionality
- **User Management**: Registration, authentication, profile management
- **Ride Management**: Create, search, book, and manage rides
- **Vehicle Management**: Driver vehicle registration and management
- **Wallet System**: Digital wallet with transaction history
- **Rating System**: User-to-user rating and review system
- **Real-time Updates**: Ride status tracking and notifications

### Technical Features
- **Layered Architecture**: Models → Repositories → Services → Controllers
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access**: Driver and Passenger role management
- **Advanced Search**: Filter rides by location, price, amenities, and preferences
- **File Upload**: Profile picture and document upload support
- **Database Relationships**: Comprehensive SQLAlchemy models with proper relationships

## 🏗️ Architecture

```
app/
├── models/              # Database models (SQLAlchemy)
│   ├── user.py
│   ├── vehicle.py
│   ├── ride.py
│   ├── ride_request.py
│   ├── transaction.py
│   ├── rating.py
│   └── payment.py
├── repositories/        # Data access layer
├── services/           # Business logic layer
├── controllers/        # HTTP request handlers
├── schemas.py          # Pydantic models for API
├── database.py         # Database configuration
└── main.py            # FastAPI application entry point
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sobia113/RideShare-Backend.git
   cd RideShare-Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DATABASE_URL=sqlite:///./rideshare.db
   
   # JWT Configuration  
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Application Configuration
   ENVIRONMENT=development
   DEBUG=True
   
   # Upload Configuration
   UPLOAD_DIR=uploads
   MAX_FILE_SIZE=5242880  # 5MB in bytes
   
   # For MySQL (recommended for production)
   # DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/rideshare_db
   
   # MySQL Workbench Connection Details:
   # Host: localhost
   # Port: 3306  
   # Username: root (or your MySQL username)
   # Password: your_mysql_password
   # Database: rideshare_db
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/reset-password` - Password reset

### User Management
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `POST /users/profile/setup` - Complete profile setup
- `PUT /users/role` - Select user role (driver/passenger)
- `POST /users/wallet/add-money` - Add money to wallet

### Rides
- `POST /rides/` - Create new ride (drivers only)
- `GET /rides/search` - Search available rides
- `GET /rides/my-rides` - Get user's rides
- `PUT /rides/{ride_id}/status` - Update ride status

### Ride Requests
- `POST /ride-requests/` - Book a ride
- `GET /ride-requests/my-requests` - Get user's ride requests
- `PUT /ride-requests/{request_id}/accept` - Accept ride request
- `PUT /ride-requests/{request_id}/reject` - Reject ride request

### Vehicles
- `POST /vehicles/` - Register vehicle
- `GET /vehicles/my-vehicles` - Get user's vehicles
- `PUT /vehicles/{vehicle_id}` - Update vehicle info

### Ratings
- `POST /ratings/` - Rate a user
- `GET /ratings/received` - Get received ratings
- `GET /ratings/given` - Get given ratings

## 🗃️ Database Schema

### Core Models
- **User**: User account information, wallet, ratings
- **Vehicle**: Driver vehicle details
- **Ride**: Ride postings with source, destination, timing
- **RideRequest**: Passenger booking requests
- **Transaction**: Wallet transaction history
- **Rating**: User-to-user ratings and reviews
- **Payment**: Payment processing records

### Key Relationships
- Users can have multiple vehicles (1:N)
- Users can create multiple rides (1:N)
- Rides can have multiple requests (1:N)
- Users can rate multiple users (M:N)
- Transactions are linked to users and rides

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Database Setup
The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for database migrations.

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

## 🚀 Deployment

### Using Docker (Coming Soon)
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Manual Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Install dependencies
4. Run with a production WSGI server like Gunicorn

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust ORM capabilities
- Pydantic for data validation
- The Python community for continuous innovation

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact [your-email@example.com].

---

**Built with ❤️ using FastAPI** 