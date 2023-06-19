# Разброс по маркам
SELECT brand, COUNT(brand) qty
FROM ArmenCar
GROUP BY brand
ORDER BY qty DESC

# Самые популярные машины
SELECT brand, car, COUNT(car) qty
FROM ArmenCar
GROUP BY brand, car
ORDER BY qty DESC

# Средняя цена по маркам
SELECT car, `year`, mileage, AVG(price)
FROM ArmenCar
GROUP BY car, `year`, mileage
ORDER BY car

# Разница от средней цены
WITH prise_avg AS
(SELECT car, `year`, mileage, AVG(price) avg_p
FROM ArmenCar
GROUP BY car, `year`, mileage
ORDER BY car)

SELECT A.car, A.`year`, A.mileage, A.price, avg_p, (A.price - avg_p) diff
FROM ArmenCar A LEFT JOIN prise_avg P ON A.car=P.car AND A.`year`=P.`year` AND A.mileage=P.mileage
ORDER BY car