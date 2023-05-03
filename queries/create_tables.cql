CREATE TABLE IF NOT EXISTS rental_properties (
    id UUID,
    name TEXT,
    description TEXT,
    address TEXT,
    bedrooms INT,
    bathrooms INT,
    price DECIMAL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS rental_bookings (
    id UUID,
    rental_id UUID,
    start_date DATE,
    end_date DATE,
    user_id UUID,
    PRIMARY KEY (id, rental_id)
);
CREATE TABLE IF NOT EXISTS rental_reviews (
    id UUID,
    rental_id UUID,
    user_id UUID,
    rating INT,
    comment TEXT,
    PRIMARY KEY (id, rental_id)
);
CREATE TABLE IF NOT EXISTS users (
    id UUID,
    name TEXT,
    PRIMARY KEY (id)
);
