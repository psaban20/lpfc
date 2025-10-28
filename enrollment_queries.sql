/** Program Player Count */
SELECT TOP (100) PERCENT [Program Name], COUNT([Player Id]) AS [Player Count]
FROM   dbo.Enrollment_Details
GROUP BY [Program Name], [Program Year], [Program Sort Order]
HAVING [Program Sort Order] > 0
ORDER BY [Program Year], [Program Sort Order]

/** Program Year, Unique Player Count, Unique Family Count **/
SELECT a.[Program Year], a.cnt as [Unique Player Count], b.cnt as [UniqueFamily Count]
FROM
( 
SELECT TOP (100) PERCENT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS cnt, dbo.AthleticPrograms.[Program Year]
FROM   dbo.Enrollment_Details INNER JOIN
             dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
GROUP BY dbo.AthleticPrograms.[Program Year]
--HAVING (dbo.AthleticPrograms.[Program Year] = 2024)
) a
INNER JOIN
( 
SELECT TOP (100) PERCENT COUNT(DISTINCT dbo.Enrollment_Details.[User Id]) AS cnt, dbo.AthleticPrograms.[Program Year]
FROM   dbo.Enrollment_Details INNER JOIN
             dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
GROUP BY dbo.AthleticPrograms.[Program Year]
--HAVING (dbo.AthleticPrograms.[Program Year] = 2024) 
) b
ON a.[Program Year]=b.[Program Year]


/** Program Name, Unique Player Count, Unique Family Count **/
SELECT a.[Program Name], a.cnt as [Player Count], b.cnt as [Family Count]
FROM
( 
SELECT TOP (100) PERCENT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS cnt, dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Environment], 
             dbo.AthleticPrograms.[Program Format]
FROM   dbo.Enrollment_Details INNER JOIN
             dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID INNER JOIN
             dbo.ProgramDivisions ON dbo.AthleticPrograms.ProgramID = dbo.ProgramDivisions.ProgramID
WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
GROUP BY dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Environment], dbo.AthleticPrograms.[Program Format], dbo.Enrollment_Details.[Program Sort Order]
--HAVING (dbo.AthleticPrograms.[Program Year] = 2024)
ORDER BY dbo.Enrollment_Details.[Program Sort Order]
) a
INNER JOIN
( 
SELECT TOP (100) PERCENT COUNT(DISTINCT dbo.Enrollment_Details.[User Id]) AS cnt, dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Environment], 
             dbo.AthleticPrograms.[Program Format]
FROM   dbo.Enrollment_Details INNER JOIN
             dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID INNER JOIN
             dbo.ProgramDivisions ON dbo.AthleticPrograms.ProgramID = dbo.ProgramDivisions.ProgramID
WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
GROUP BY dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Environment], dbo.AthleticPrograms.[Program Format], dbo.Enrollment_Details.[Program Sort Order]
--HAVING (dbo.AthleticPrograms.[Program Year] = 2024)
ORDER BY dbo.Enrollment_Details.[Program Sort Order]  
) b
ON a.[Program Name]=b.[Program Name]


/** Program, Divsion and Player count **/
SELECT TOP (100) PERCENT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS [Players 2022], dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Format], 
             dbo.AthleticPrograms.[Program Environment], dbo.ProgramDivisions.[Division Name], dbo.ProgramDivisions.[Division Gender]
FROM   dbo.Enrollment_Details INNER JOIN
             dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID INNER JOIN
             dbo.ProgramDivisions ON dbo.AthleticPrograms.ProgramID = dbo.ProgramDivisions.ProgramID AND dbo.Enrollment_Details.[Division Name] = dbo.ProgramDivisions.[Division Name]
WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
GROUP BY dbo.AthleticPrograms.[Program Year], dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Season], dbo.AthleticPrograms.[Program Format], dbo.AthleticPrograms.[Program Environment], dbo.ProgramDivisions.[Division Name], 
             dbo.ProgramDivisions.[Division Gender]


SELECT COUNT(DISTINCT [Player Id]) as [Players Lifetime]
FROM   dbo.Enrollment_Details

SELECT COUNT(DISTINCT [User Id]) as [Families Lifetime]
FROM   dbo.Enrollment_Details

SELECT COUNT(DISTINCT [Player Id]) AS [Players 2022]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2022-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2022-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [User Id]) AS [Families 2022]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2022-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2022-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [Player Id]) AS [Players 2023]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2023-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2023-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [User Id]) AS [Families 2023]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2023-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2023-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [Player Id]) AS [Players 2024]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2024-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2024-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [User Id]) AS [Families 2024]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2024-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2024-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [Player Id]) AS [Players 2025]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2025-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2025-12-31 00:00:00', 102))

SELECT COUNT(DISTINCT [User Id]) AS [Families 2025]
FROM   dbo.Enrollment_Details
WHERE ([Order Date] BETWEEN CONVERT(DATETIME, '2025-01-01 00:00:00', 102) AND CONVERT(DATETIME, '2025-12-31 00:00:00', 102))