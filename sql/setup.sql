CREATE DATABASE IF NOT EXISTS storedb;
USE storedb;
-- revenue by the regions
SELECT Region, SUM(TotalAmount) AS revenue
FROM orders
GROUP BY Region
ORDER BY revenue DESC;
CREATE TABLE IF NOT EXISTS orders (
    OrderID VARCHAR(50),
    CustomerID VARCHAR(20),
    Category VARCHAR(50),
    Quantity INT,
    UnitPrice DECIMAL (10, 2),
    TotalAmount DECIMAL (10, 2),
    PaymentMethod VARCHAR(50),
    Region VARCHAR(100),
    OrderDate DATE
);

