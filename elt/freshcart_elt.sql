-- FreshCart ELT Pipeline (Bronze -> Silver/Quarantine -> Gold + SCD2 + DQ)
CREATE OR REPLACE DATABASE FRESHCART_DB;
USE DATABASE FRESHCART_DB;
CREATE OR REPLACE SCHEMA ELT;
USE SCHEMA ELT;

CREATE OR REPLACE TABLE BRONZE_ORDERS (
    order_id STRING, customer_id STRING, customer_tier STRING,
    amount FLOAT, currency STRING, status STRING, event_ts TIMESTAMP
);

CREATE OR REPLACE TABLE QUARANTINE_ORDERS AS
SELECT *,
       CASE
           WHEN amount <= 0 OR amount IS NULL THEN 'INVALID_AMOUNT'
           WHEN currency NOT IN ('INR', 'USD', 'EUR') OR currency IS NULL THEN 'INVALID_CURRENCY'
       END AS reject_reason
FROM BRONZE_ORDERS
WHERE amount <= 0 OR amount IS NULL OR currency NOT IN ('INR', 'USD', 'EUR') OR currency IS NULL;

CREATE OR REPLACE TABLE SILVER_ORDERS AS
SELECT DISTINCT order_id, customer_id, customer_tier, amount, currency, status, event_ts
FROM BRONZE_ORDERS
WHERE amount > 0 AND currency IN ('INR', 'USD', 'EUR');

CREATE OR REPLACE TABLE GOLD_REVENUE AS
SELECT customer_tier, COUNT(*) AS total_orders, SUM(amount) AS total_revenue
FROM SILVER_ORDERS
WHERE status = 'DELIVERED'
GROUP BY customer_tier;
