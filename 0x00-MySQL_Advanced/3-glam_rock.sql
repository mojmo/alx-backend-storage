-- This script lists Glam Rock bands ranked by their longevity (years active).

SELECT band_name AS band_name, IFNULL(split, 2022) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
-- Filter bands with 'Glam Rock' style
WHERE style LIKE '%Glam rock%'
-- Order by lifespan (descending)
ORDER BY lifespan DESC;
