# 💰 Expense Management System

A full-stack expense tracking application with advanced analytics capabilities, built with FastAPI backend and Streamlit frontend. Designed with scalability and future AI/ML integration in mind.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

### Demo
https://project-expense-tracking.streamlit.app

## 🎯 Features

### 🔐 Authentication
- User registration and login system
- JWT token-based authentication
- Secure password hashing with bcrypt

### 💸 Expense Management
- Add, view, and manage daily expenses
- Categorize expenses (Food, Rent, Entertainment, Shopping, Other)
- Add notes and descriptions for each expense
- Date-based expense filtering
- Bulk expense operations

### 📊 Advanced Analytics
- **Category Analytics**: Spending breakdown by category with percentages
- **Monthly Trends**: Visualize spending patterns over time
- **Interactive Charts**: Plotly-powered visualizations
- **Date Range Filtering**: Customizable analysis periods

### 🎨 Modern UI/UX
- Responsive design with gradient styling
- Interactive dashboard with real-time metrics
- Tab-based navigation for different functionalities
- Professional color scheme and layout

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **JWT** - JSON Web Tokens for secure authentication
- **Passlib** - Password hashing with bcrypt
- **MySQL Connector** - Database driver
- **Uvicorn** - ASGI server for production deployment

### Frontend
- **Streamlit** - Rapid web application development
- **Plotly** - Interactive data visualizations
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API communication

### Database
- **MySQL** - Relational database management system
- **Optimized Schema** with proper indexing and relationships

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/yourusername/expense-management-system.git
cd expense-management-system

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

-- Create database
CREATE DATABASE expense_manager;

-- Create user (optional)
CREATE USER 'expense_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON expense_manager.* TO 'expense_user'@'localhost';
FLUSH PRIVILEGES;

# Navigate to frontend directory
cd frontend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

#start backend server
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

#start frontend application
cd frontend
source venv/bin/activate
streamlit run app.py
```

### 📊 API Endpoints

**Authentication**

- POST /create_user/ - Create new user account
- POST /login/ - User login and JWT token generation
- Expenses

- GET /expenses/ - Get expenses for specific date
- POST /expenses/ - Add or update expenses
- Analytics

- POST /analytics/ - Get category-wise spending analytics
- GET /analytics_by_month/ - Get monthly spending trends


### 🗃️ Database Schema

**User Table**
```commandline
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
```commandline
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, expense_date),
    INDEX idx_category (category)
);
```


### 🎨 Usage Guide

##### 1. Registration & Login

- Open the Streamlit application
- Create a new account or login with existing credentials
- JWT tokens are automatically handled by the application

##### 2. Adding Expenses

- Navigate to the "Add/Update Expenses" tab
- Select the date for your expenses
- Fill in amount, category, and notes for each expense
- Submit to save to the database

##### 3. Viewing Analytics

- Use the "Category Analytics" tab for spending breakdowns
- Use the "Monthly Trends" tab for time-based analysis
- Customize date ranges for specific insights

### 🔧 Configuration

##### Environment Variables (Backend)

Create a .env file in the backend directory:
```commandline
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/expense_manager
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
##### Database Configuration

Edit the database connection in db_helper.py if needed:
```commandline
mysql_connection = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='expense_manager'
)
```

### 🧪 Testing

##### Running Tests
```commandline
# Backend tests
cd backend
python -m pytest

# API testing with curl examples
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

### 🚀 Deployment

##### Production Deployment with Docker

```commandline
# Dockerfile for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options

- Backend: AWS EC2, Google Cloud Run, Heroku
- Frontend: Streamlit Cloud, Heroku, Vercel
- Database: AWS RDS, Google Cloud SQL, Azure Database for MySQL


### 🔮 Future Enhancements

##### Planned Features

- ML Integration: Spending prediction and anomaly detection
- Budget Management: Set and track spending limits
- Receipt Upload: Image processing for expense tracking
- Data Export: CSV/PDF reports generation
- Mobile App: React Native companion app
- Multi-currency Support: International expense tracking
  
##### AI/ML Capabilities

- Time series forecasting for future spending
- Natural language processing for automatic category tagging
- Anomaly detection for unusual spending patterns
- Personalized budget recommendations

### 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

#### Development Setup

- Fork the repository
- Create a feature branch (git checkout -b feature/amazing-feature)
- Commit your changes (git commit -m 'Add amazing feature')
- Push to the branch (git push origin feature/amazing-feature)
- Open a Pull Request




