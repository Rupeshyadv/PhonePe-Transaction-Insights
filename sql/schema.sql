-- Aggregated Tables

CREATE TABLE aggregated_user (
    state VARCHAR(100),
    year INT,
    quarter INT,
    brand VARCHAR(100),
    user_count BIGINT,
    percentage FLOAT
);

CREATE TABLE aggregated_transaction (
    state VARCHAR(100),
    year INT,
    quarter INT,
    transaction_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

CREATE TABLE aggregated_insurance (
    state VARCHAR(100),
    year INT,
    quarter INT,
    insurance_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- Map Tables

CREATE TABLE map_user (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    registered_users BIGINT,
    app_opens BIGINT
);

CREATE TABLE map_transaction (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

CREATE TABLE map_insurance (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- Top Tables

CREATE TABLE top_user (
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    year INT,
    quarter INT,
    registered_users BIGINT
);

CREATE TABLE top_transaction (
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

CREATE TABLE top_insurance (
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);