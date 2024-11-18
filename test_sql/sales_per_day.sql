
SELECT 
    date , 
    SUM(prod_price*prod_qty) as ventes
FROM TRANSACTION 
WHERE date between '01/01/2019' AND '31/12/2019'
GROUP BY Date
ORDER BY Date 

