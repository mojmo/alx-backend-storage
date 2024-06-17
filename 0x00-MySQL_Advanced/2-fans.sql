-- This script ranks country origins of bands based on the number of non-unique fans.

-- Count fans for each origin (non-unique)
SELECT origin, COUNT(*) AS nb_fans
-- Source table
FROM metal_bands
-- Group rows by origin
GROUP BY origin
-- Order by fan count (descending)
ORDER BY nb_fans DESC;
