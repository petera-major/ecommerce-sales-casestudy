USE storedb;

SELECT COUNT(*) AS total_orders FROM orders;
SELECT * FROM orders LIMIT 10;

-- revenue in total
SELECT Category, SUM(TotalAmount) AS revenue
FROM orders
GROUP BY Category
ORDER BY revenue DESC
LIMIT 5;

-- revenue by the regions
SELECT Region, SUM(TotalAmount) AS revenue
FROM orders
GROUP BY Region
ORDER BY revenue DESC;

-- sales by the season
SELECT CASE
WHEN MONTH(OrderDate) IN (3,4,5,6) THEN 'Spring'
WHEN MONTH(OrderDate) IN (7,8) THEN 'Summer'
WHEN MONTH(OrderDate) IN (9,10,11) THEN 'Fall'
ELSE 'Winter'
END AS Season,
SUM(TotalAmount) AS revenue
FROM orders
GROUP BY Season
ORDER BY revenue DESC;
