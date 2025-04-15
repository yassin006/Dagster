SELECT
    day,
    AVG(tmin) AS avg_tmin,
    AVG(tmax) AS avg_tmax
FROM {{ ref('weather_model') }}
GROUP BY day
ORDER BY day
