-- Step 3 — Urban Threads database schema
-- Run this after creating the database: psql -d urban_threads -f sql/schema.sql

DROP TABLE IF EXISTS returns CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS discounts CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

CREATE TABLE stores (
    store_id     INTEGER PRIMARY KEY,
    store_name   VARCHAR(100) NOT NULL,
    city         VARCHAR(50) NOT NULL,
    channel      VARCHAR(20) NOT NULL CHECK (channel IN ('Store', 'Online'))
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    cost_price   NUMERIC(10, 2) NOT NULL CHECK (cost_price >= 0),
    sale_price   NUMERIC(10, 2) NOT NULL CHECK (sale_price >= 0)
);

CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    email        VARCHAR(150) UNIQUE NOT NULL,
    city         VARCHAR(50),
    signup_date  DATE NOT NULL,
    segment      VARCHAR(20) CHECK (segment IN ('New', 'Regular', 'VIP', 'Lapsed'))
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    store_id     INTEGER NOT NULL REFERENCES stores(store_id),
    order_date   DATE NOT NULL,
    channel      VARCHAR(20) NOT NULL,
    order_total  NUMERIC(10, 2) NOT NULL CHECK (order_total >= 0)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(10, 2) NOT NULL,
    line_total    NUMERIC(10, 2) NOT NULL
);

CREATE TABLE inventory (
    inventory_id   INTEGER PRIMARY KEY,
    store_id       INTEGER NOT NULL REFERENCES stores(store_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    stock_on_hand  INTEGER NOT NULL CHECK (stock_on_hand >= 0),
    reorder_level  INTEGER NOT NULL,
    snapshot_date  DATE NOT NULL
);

CREATE TABLE returns (
    return_id      INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    order_item_id  INTEGER NOT NULL REFERENCES order_items(order_item_id),
    return_date    DATE NOT NULL,
    reason         VARCHAR(50),
    refund_amount  NUMERIC(10, 2) NOT NULL
);

CREATE TABLE discounts (
    campaign_code  VARCHAR(30) PRIMARY KEY,
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL,
    discount_pct   NUMERIC(4, 2) NOT NULL
);

-- Helpful indexes for the KPI queries in kpi_queries.sql
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_store ON orders(store_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_returns_order ON returns(order_id);
