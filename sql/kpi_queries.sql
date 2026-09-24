-- Step 3 — KPI queries for Urban Threads
-- Run individually in psql/pgAdmin, or reuse in Step 4/6 as needed.

-- 1. Total revenue by region (store city) and channel
SELECT
    s.city,
    s.channel,
    ROUND(SUM(o.order_total), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.city, s.channel
ORDER BY revenue DESC;

-- 2. Revenue trend by month
SELECT
    DATE_TRUNC('month', order_date)::date AS month,
    ROUND(SUM(order_total), 2) AS revenue,
    COUNT(*) AS order_count
FROM orders
GROUP BY month
ORDER BY month;

-- 3. Average Order Value (AOV), overall and by channel
SELECT
    channel,
    ROUND(AVG(order_total), 2) AS avg_order_value,
    COUNT(*) AS order_count
FROM orders
GROUP BY channel;

-- 4. Revenue by product category
SELECT
    p.category,
    ROUND(SUM(oi.line_total), 2) AS revenue,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 5. Return rate (%) overall and by store
SELECT
    s.city,
    COUNT(DISTINCT r.return_id)::numeric / NULLIF(COUNT(DISTINCT oi.order_item_id), 0) * 100 AS return_rate_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN stores s ON o.store_id = s.store_id
LEFT JOIN returns r ON r.order_item_id = oi.order_item_id
GROUP BY s.city
ORDER BY return_rate_pct DESC;

-- 6. Return reasons breakdown
SELECT
    reason,
    COUNT(*) AS return_count,
    ROUND(SUM(refund_amount), 2) AS total_refunded
FROM returns
GROUP BY reason
ORDER BY return_count DESC;

-- 7. Inventory turnover proxy: stock on hand vs. reorder level, by store
SELECT
    s.city,
    COUNT(*) FILTER (WHERE i.stock_on_hand <= i.reorder_level) AS low_stock_skus,
    COUNT(*) AS total_skus_stocked
FROM inventory i
JOIN stores s ON i.store_id = s.store_id
GROUP BY s.city
ORDER BY low_stock_skus DESC;

-- 8. Customer segment revenue contribution
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(o.order_total), 2) AS revenue,
    ROUND(SUM(o.order_total) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.segment
ORDER BY revenue DESC;

-- 9. Repeat purchase rate: customers with more than one order
SELECT
    COUNT(*) FILTER (WHERE order_count > 1)::numeric / COUNT(*) * 100 AS repeat_purchase_rate_pct
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) sub;

-- 10. The Melbourne dip — quarterly revenue for Melbourne vs. other stores
-- (This is the pattern the Step 7 AI layer will be asked to explain later)
SELECT
    DATE_TRUNC('quarter', o.order_date)::date AS quarter,
    s.city,
    ROUND(SUM(o.order_total), 2) AS revenue
FROM orders o
JOIN stores s ON o.store_id = s.store_id
WHERE s.channel = 'Store'
GROUP BY quarter, s.city
ORDER BY quarter, s.city;
