# QuickCourt 🏟️

A comprehensive sports venue booking and management system built with Flask, enabling users to discover, book, and manage sports court reservations online.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [System Workflow](#system-workflow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)

## ✨ Features

### User Management
- **Multi-role Authentication**: Support for Users, Venue Owners, and Admins
- **Secure Registration**: Email-based OTP verification
- **Password Recovery**: Forgot password with OTP-based reset
- **Profile Management**: User profile with avatar support
- **Session Management**: Secure session handling with Flask sessions

### Booking System
- **Venue Discovery**: Browse available sports venues
- **Court Booking**: Reserve courts with date/time selection
- **Booking History**: View and manage personal bookings
- **Real-time Availability**: Check court availability

### Admin Features
- **User Management**: View and manage all users
- **Venue Oversight**: Monitor all venues and bookings
- **System Analytics**: Dashboard with key metrics

### Owner Features
- **Venue Management**: Add and manage owned venues
- **Booking Management**: View and manage court bookings
- **Revenue Tracking**: Monitor booking revenue

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │  Owners  │  │  Admins  │  │ Browsers │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                          │
                    HTTP/HTTPS
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                  PRESENTATION LAYER                        │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Flask Web Framework (app.py)               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐  │   │
│  │  │  Routes  │  │ Sessions │  │  Authentication │  │   │
│  │  └──────────┘  └──────────┘  └─────────────────┘  │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                   BUSINESS LOGIC LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Auth Handler │  │ OTP Service  │  │ Email Service│    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │Booking Logic │  │ Venue Manager│  │ User Manager │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                     DATA LAYER                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │         SQLite Database (quickcourt.db)            │   │
│  │  ┌──────┐  ┌────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │Users │  │ Venues │  │ Bookings│  │ Courts  │  │   │
│  │  └──────┘  └────────┘  └─────────┘  └─────────┘  │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                   EXTERNAL SERVICES                        │
│  ┌────────────────────────────────────────────────────┐   │
│  │        Gmail SMTP Server (Email Service)           │   │
│  │          - OTP Delivery                            │   │
│  │          - Notifications                           │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

## 🔄 System Workflow

### User Registration Flow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────────┐
│ User fills      │
│ signup form     │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ System hashes   │
│ password        │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Generate 4-digit│
│ OTP             │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Store temp data │
│ in session      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Send OTP via    │
│ email (SMTP)    │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ User enters OTP │
└────┬────────────┘
     │
     ▼
┌─────────────────┐      ┌─────────────┐
│ Verify OTP      │─────►│ Invalid OTP │
└────┬────────────┘ No   └─────────────┘
     │ Yes
     ▼
┌─────────────────┐
│ Insert user     │
│ into database   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Clear session   │
│ data            │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Redirect to     │
│ Login           │
└────┬────────────┘
     │
     ▼
┌─────────┐
│   End   │
└─────────┘
```

### Login & Dashboard Routing Flow

```
┌─────────┐
│  Login  │
└────┬────┘
     │
     ▼
┌──────────────────┐
│ Enter email &    │
│ password         │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Hash password    │
│ & query DB       │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐      ┌─────────────────┐
│ User found?      │─────►│ Invalid Login   │
└────┬─────────────┘ No   └─────────────────┘
     │ Yes
     ▼
┌──────────────────┐
│ Store user data  │
│ in session       │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Check user role  │
└────┬─────────────┘
     │
     ├────────────┬─────────────┬──────────────┐
     │            │             │              │
     ▼            ▼             ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌─────────┐
│  User   │  │  Owner  │  │  Admin   │  │ Invalid │
│Dashboard│  │Dashboard│  │Dashboard │  │  Role   │
└─────────┘  └─────────┘  └──────────┘  └─────────┘
```

### Password Reset Flow

```
┌──────────────┐
│ Forgot       │
│ Password     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Enter email  │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌────────────────┐
│ Email exists?│─────►│ Email not found│
└──────┬───────┘ No   └────────────────┘
       │ Yes
       ▼
┌──────────────┐
│ Generate OTP │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Store email  │
│ in session   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Send OTP     │
│ via email    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Enter OTP &  │
│ new password │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌────────────┐
│ Verify OTP   │─────►│ Wrong OTP  │
└──────┬───────┘ No   └────────────┘
       │ Yes
       ▼
┌──────────────┐
│ Update       │
│ password     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Clear session│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Redirect to  │
│ Login        │
└──────────────┘
```

## 📁 Project Structure

```
quickcourt/
│
├── app.py                      # Main Flask application
├── init_db.py                  # Database initialization script
├── schema.sql                  # Database schema
├── requirements.txt            # Python dependencies
├── quickcourt.db              # SQLite database
│
├── static/                    # Static assets
│   ├── css/
│   ├── js/
│   ├── images/
│   └── avatars/
│       └── default.png
│
└── templates/                 # HTML templates
    ├── home.html
    ├── login.html
    ├── signup.html
    ├── verify_otp.html
    ├── forgot.html
    ├── reset_password.html
    ├── user_dashboard.html
    ├── owner_dashboard.html
    ├── admin_dashboard.html
    ├── venues.html
    ├── single_venue.html
    ├── court_booking.html
    ├── profile.html
    └── my_bookings.html
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- SQLite3
- Gmail account (for SMTP)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quickcourt.git
   cd quickcourt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Configure email settings**
   - Update `app.py` with your Gmail credentials
   - Generate an App Password from Google Account settings

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open browser: `http://localhost:5000`

## ⚙️ Configuration

### Email Configuration

Update the following in `app.py`:

```python
sender = "your-email@gmail.com"
password = "your-app-password"  # Gmail App Password
```

### Secret Key

For production, change the secret key:

```python
app.secret_key = "your-secure-random-key"
```

### Database

The SQLite database is created automatically. For production, consider PostgreSQL or MySQL.

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'owner', 'admin')),
    avatar TEXT DEFAULT 'default.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Venues Table
```sql
CREATE TABLE venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    venue_id INTEGER,
    court_id INTEGER,
    booking_date DATE,
    start_time TIME,
    end_time TIME,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (venue_id) REFERENCES venues(id)
);
```

## 🔒 Security Features

- **Password Hashing**: SHA-256 encryption for all passwords
- **OTP Verification**: 4-digit OTP for registration and password reset
- **Session Management**: Secure Flask sessions
- **Role-Based Access Control**: User, Owner, and Admin roles
- **SQL Injection Prevention**: Parameterized queries
- **HTTPS Support**: SSL/TLS for email communication

## 📝 Usage

### Default Admin Credentials

```
Email: admin@quickcourt.com
Password: Admin@123
```

### User Roles

1. **User**
   - Browse venues
   - Book courts
   - View booking history
   - Manage profile

2. **Owner**
   - All user features
   - Add/manage venues
   - View venue bookings
   - Revenue tracking

3. **Admin**
   - All owner features
   - User management
   - System oversight
   - Analytics dashboard

## 🔮 Future Enhancements

- [ ] Payment gateway integration
- [ ] Real-time availability calendar
- [ ] Push notifications
- [ ] Mobile app (React Native)
- [ ] Advanced search and filters
- [ ] Ratings and reviews
- [ ] Loyalty programs
- [ ] Multi-language support
- [ ] Social media integration
- [ ] Analytics and reporting dashboard

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 📧 Contact

For questions or support, please contact: support@quickcourt.com

---

**QuickCourt** - Making sports booking simple and efficient! 🏆
