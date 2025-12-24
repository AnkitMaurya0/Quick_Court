DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS facilities;
DROP TABLE IF EXISTS facility_photos;
DROP TABLE IF EXISTS courts;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS blocked_slots;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS facility_sports;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    avatar TEXT,
    role TEXT NOT NULL CHECK(role IN ('user','owner','admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    short_location TEXT,
    is_approved INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE facility_photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    photo_path TEXT NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES facilities(id)
);

CREATE TABLE courts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    sport_type TEXT NOT NULL,
    price_per_hour REAL NOT NULL,
    open_time TEXT,
    close_time TEXT,
    FOREIGN KEY (facility_id) REFERENCES facilities(id)
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    court_id INTEGER NOT NULL,
    start_dt TEXT NOT NULL,
    end_dt TEXT NOT NULL,
    status TEXT DEFAULT 'confirmed' CHECK(status IN ('confirmed','cancelled','completed')),
    amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (court_id) REFERENCES courts(id)
);

CREATE TABLE blocked_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    court_id INTEGER NOT NULL,
    start_dt TEXT NOT NULL,
    end_dt TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY (court_id) REFERENCES courts(id)
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE amenities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES facilities(id)
);

CREATE TABLE facility_sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id INTEGER NOT NULL,
    sport_type TEXT NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES facilities(id)
);
