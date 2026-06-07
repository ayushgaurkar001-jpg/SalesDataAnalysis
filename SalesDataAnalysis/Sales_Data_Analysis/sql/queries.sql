-- ============================================================
-- Sales Analysis SQL Queries
-- Database: sales_analysis
-- ============================================================

CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

-- Create table
CREATE TABLE IF NOT EXISTS sales (
    OrderID     VARCHAR(20) PRIMARY KEY,
    OrderDate   DATE,
    CustomerID  VARCHAR(20),
    CustomerName VARCHAR(100),
    ProductName VARCHAR(100),
    Category    VARCHAR(50),
    SubCategory VARCHAR(50),
    Quantity    INT,
    Sales       DECIMAL(12,2),
    Profit      DECIMAL(12,2),
    Region      VARCHAR(20),
    State       VARCHAR(50)
);

-- 1. Total Sales & Profit
SELECT
    ROUND(SUM(Sales), 2)  AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS OverallMarginPct
FROM sales;

-- 2. Monthly Sales Trend
SELECT
    YEAR(OrderDate)  AS Year,
    MONTH(OrderDate) AS Month,
    MONTHNAME(OrderDate) AS MonthName,
    ROUND(SUM(Sales), 2) AS MonthlySales,
    ROUND(SUM(Profit),2) AS MonthlyProfit
FROM sales
GROUP BY YEAR(OrderDate), MONTH(OrderDate), MONTHNAME(OrderDate)
ORDER BY Year, Month;

-- 3. Top 10 Products by Revenue
SELECT
    ProductName,
    ROUND(SUM(Sales), 2)  AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    SUM(Quantity)         AS UnitsSold
FROM sales
GROUP BY ProductName
ORDER BY TotalSales DESC
LIMIT 10;

-- 4. Top 10 Customers by Spending
SELECT
    CustomerID,
    CustomerName,
    ROUND(SUM(Sales), 2)     AS TotalSpend,
    COUNT(DISTINCT OrderID)  AS OrderCount,
    ROUND(AVG(Sales), 2)     AS AvgOrderValue
FROM sales
GROUP BY CustomerID, CustomerName
ORDER BY TotalSpend DESC
LIMIT 10;

-- 5. Region-wise Sales Analysis
SELECT
    Region,
    ROUND(SUM(Sales), 2)  AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    COUNT(DISTINCT OrderID) AS Orders,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS MarginPct
FROM sales
GROUP BY Region
ORDER BY TotalSales DESC;

-- 6. Category-wise Profit Analysis
SELECT
    Category,
    SubCategory,
    ROUND(SUM(Sales), 2)  AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS MarginPct
FROM sales
GROUP BY Category, SubCategory
ORDER BY Category, TotalProfit DESC;

-- 7. Best Performing Products (by Profit)
SELECT ProductName, Category,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(Profit),2) AS Profit
FROM sales
GROUP BY ProductName, Category
ORDER BY Profit DESC LIMIT 10;

-- 8. Worst Performing Products (by Profit)
SELECT ProductName, Category,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(Profit),2) AS Profit
FROM sales
GROUP BY ProductName, Category
ORDER BY Profit ASC LIMIT 10;

-- 9. State-wise performance
SELECT State, Region,
    ROUND(SUM(Sales),2) AS TotalSales,
    ROUND(SUM(Profit),2) AS TotalProfit
FROM sales
GROUP BY State, Region
ORDER BY TotalSales DESC;

-- 10. Yearly Growth
SELECT YEAR(OrderDate) AS Year,
    ROUND(SUM(Sales),2) AS TotalSales,
    ROUND(SUM(Profit),2) AS TotalProfit,
    COUNT(DISTINCT OrderID) AS Orders
FROM sales
GROUP BY Year ORDER BY Year;
