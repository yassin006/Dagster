-- models/weather_model.sql

SELECT 
    day,
    tmin,
    tmax,
    weather
FROM weather
WHERE tmax > 15
ORDER BY day
