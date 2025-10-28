from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from app.database import db
from app.models import (
    AthleticProgram,
    ProgramDivision,
    EnrollmentDetail,
    ProgramStats,
    YearStats,
    DivisionStats,
    PlayerEnrollmentStats
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LPFC Athletic Programs API",
    description="API for managing athletic programs, divisions, and enrollments",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "LPFC Athletic Programs API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    try:
        db.execute_query("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Athletic Programs Endpoints
@app.get("/programs", response_model=List[AthleticProgram])
def get_programs(year: Optional[int] = None):
    """Get all athletic programs, optionally filtered by year"""
    try:
        query = "SELECT * FROM [dbo].[AthleticPrograms]"
        if year:
            query += f" WHERE [Program Year] = {year}"
        query += " ORDER BY [Program Sort Order], [Program Year] DESC"

        results = db.execute_query(query)

        # Convert space-separated column names to PascalCase
        formatted_results = []
        for row in results:
            formatted_row = {
                "ProgramID": row.get("ProgramID"),
                "ProgramName": row.get("Program Name"),
                "ProgramSport": row.get("Program Sport"),
                "ProgramYear": row.get("Program Year"),
                "ProgramSeason": row.get("Program Season"),
                "ProgramFormat": row.get("Program Format"),
                "ProgramEnvironment": row.get("Program Environment"),
                "ProgramSortOrder": row.get("Program Sort Order")
            }
            formatted_results.append(formatted_row)

        return formatted_results
    except Exception as e:
        logger.error(f"Error fetching programs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/programs/{program_id}", response_model=AthleticProgram)
def get_program(program_id: int):
    """Get a specific athletic program by ID"""
    try:
        query = "SELECT * FROM [dbo].[AthleticPrograms] WHERE ProgramID = ?"
        results = db.execute_query(query, (program_id,))

        if not results:
            raise HTTPException(status_code=404, detail="Program not found")

        row = results[0]
        return {
            "ProgramID": row.get("ProgramID"),
            "ProgramName": row.get("Program Name"),
            "ProgramSport": row.get("Program Sport"),
            "ProgramYear": row.get("Program Year"),
            "ProgramSeason": row.get("Program Season"),
            "ProgramFormat": row.get("Program Format"),
            "ProgramEnvironment": row.get("Program Environment"),
            "ProgramSortOrder": row.get("Program Sort Order")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching program {program_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Program Divisions Endpoints
@app.get("/divisions", response_model=List[ProgramDivision])
def get_divisions(program_id: Optional[int] = None):
    """Get all program divisions, optionally filtered by program"""
    try:
        query = "SELECT * FROM [dbo].[ProgramDivisions]"
        params = None

        if program_id:
            query += " WHERE ProgramID = ?"
            params = (program_id,)

        results = db.execute_query(query, params)

        formatted_results = []
        for row in results:
            formatted_row = {
                "DivisionID": row.get("DivisionID"),
                "ProgramID": row.get("ProgramID"),
                "DivisionName": row.get("Division Name"),
                "DivisionFormat": row.get("Division Format"),
                "DivisionGender": row.get("Division Gender"),
                "UpperDivision": row.get("Upper Division"),
                "LowerDivision": row.get("Lower Division"),
                "DivisionDuration_Weeks": row.get("DivisionDuration_Weeks"),
                "DivisionPractices_PerWeek": row.get("DivisionPractices_PerWeek"),
                "DivisionPracticeLenth_Hours": row.get("DivisionPracticeLenth_Hours"),
                "DivisionGames_PerWeek": row.get("DivisionGames_PerWeek"),
                "DivisionGameLength_Hours": row.get("DivisionGameLength_Hours")
            }
            formatted_results.append(formatted_row)

        return formatted_results
    except Exception as e:
        logger.error(f"Error fetching divisions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enrollment Endpoints
@app.get("/enrollments", response_model=List[EnrollmentDetail])
def get_enrollments(
    program_id: Optional[int] = None,
    year: Optional[int] = None,
    limit: int = 100
):
    """Get enrollment details, optionally filtered by program and year"""
    try:
        query = "SELECT TOP (?) * FROM [dbo].[Enrollment_Details] WHERE 1=1"
        params = [limit]

        if program_id:
            query += " AND ProgramID = ?"
            params.append(program_id)

        if year:
            query += " AND [Program Year] = ?"
            params.append(year)

        query += " ORDER BY [Order Date] DESC"

        results = db.execute_query(query, tuple(params))

        formatted_results = []
        for row in results:
            formatted_row = {
                "ProgramName": row.get("Program Name"),
                "DivisionName": row.get("Division Name"),
                "AccountFirstName": row.get("Account First Name"),
                "AccountLastName": row.get("Account Last Name"),
                "PlayerFirstName": row.get("Player First Name"),
                "PlayerLastName": row.get("Player Last Name"),
                "PlayerGender": row.get("Player Gender"),
                "PlayerBirthDate": row.get("Player Birth Date"),
                "StreetAddress": row.get("Street Address"),
                "Unit": row.get("Unit"),
                "City": row.get("City"),
                "State": row.get("State"),
                "PostalCode": row.get("Postal Code"),
                "UserEmail": row.get("User Email"),
                "Telephone": row.get("Telephone"),
                "Cellphone": row.get("Cellphone"),
                "OtherPhone": row.get("Other Phone"),
                "TeamName": row.get("Team Name"),
                "OrderDate": row.get("Order Date"),
                "OrderNo": row.get("Order No"),
                "OrderDetailDescription": row.get("Order Detail Description"),
                "OrderItemAmount": row.get("OrderItem Amount"),
                "OrderItemAmountPaid": row.get("OrderItem Amount Paid"),
                "OrderItemBalance": row.get("OrderItem Balance"),
                "OrderPaymentStatus": row.get("Order Payment Status"),
                "PlayerId": row.get("Player Id"),
                "UserId": row.get("User Id"),
                "ProgramYear": row.get("Program Year"),
                "ProgramSeason": row.get("Program Season"),
                "ProgramSortOrder": row.get("Program Sort Order"),
                "DivisionGender": row.get("Division Gender"),
                "ProgramEnvironment": row.get("Program Environment"),
                "ProgramID": row.get("ProgramID")
            }
            formatted_results.append(formatted_row)

        return formatted_results
    except Exception as e:
        logger.error(f"Error fetching enrollments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Statistics Endpoints
@app.get("/stats/programs", response_model=List[ProgramStats])
def get_program_stats():
    """Get player and family counts by program"""
    try:
        query = """
        SELECT a.[Program Name] as ProgramName, a.[Program Year] as ProgramYear, a.cnt as PlayerCount, b.cnt as FamilyCount
        FROM
        (
            SELECT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS cnt,
                   dbo.AthleticPrograms.[Program Name],
                   dbo.AthleticPrograms.[Program Year]
            FROM dbo.Enrollment_Details
            INNER JOIN dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
            WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
            GROUP BY dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year]
        ) a
        INNER JOIN
        (
            SELECT COUNT(DISTINCT dbo.Enrollment_Details.[User Id]) AS cnt,
                   dbo.AthleticPrograms.[Program Name],
                   dbo.AthleticPrograms.[Program Year]
            FROM dbo.Enrollment_Details
            INNER JOIN dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
            WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
            GROUP BY dbo.AthleticPrograms.[Program Name], dbo.AthleticPrograms.[Program Year]
        ) b
        ON a.[Program Name] = b.[Program Name] AND a.[Program Year] = b.[Program Year]
        ORDER BY a.[Program Year] DESC, a.[Program Name]
        """

        results = db.execute_query(query)
        return results
    except Exception as e:
        logger.error(f"Error fetching program stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/years", response_model=List[YearStats])
def get_year_stats():
    """Get player and family counts by year"""
    try:
        query = """
        SELECT a.[Program Year] as ProgramYear,
               a.cnt as UniquePlayerCount,
               b.cnt as UniqueFamilyCount
        FROM
        (
            SELECT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS cnt,
                   dbo.AthleticPrograms.[Program Year]
            FROM dbo.Enrollment_Details
            INNER JOIN dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
            WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
            GROUP BY dbo.AthleticPrograms.[Program Year]
        ) a
        INNER JOIN
        (
            SELECT COUNT(DISTINCT dbo.Enrollment_Details.[User Id]) AS cnt,
                   dbo.AthleticPrograms.[Program Year]
            FROM dbo.Enrollment_Details
            INNER JOIN dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
            WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
            GROUP BY dbo.AthleticPrograms.[Program Year]
        ) b
        ON a.[Program Year] = b.[Program Year]
        ORDER BY a.[Program Year] ASC
        """

        results = db.execute_query(query)
        return results
    except Exception as e:
        logger.error(f"Error fetching year stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/divisions", response_model=List[DivisionStats])
def get_division_stats():
    """Get player counts by program and division"""
    try:
        query = """
        SELECT COUNT(DISTINCT dbo.Enrollment_Details.[Player Id]) AS Players,
               dbo.AthleticPrograms.[Program Year] as ProgramYear,
               dbo.AthleticPrograms.[Program Name] as ProgramName,
               dbo.AthleticPrograms.[Program Season] as ProgramSeason,
               dbo.AthleticPrograms.[Program Format] as ProgramFormat,
               dbo.AthleticPrograms.[Program Environment] as ProgramEnvironment,
               dbo.ProgramDivisions.[Division Name] as DivisionName,
               dbo.ProgramDivisions.[Division Gender] as DivisionGender
        FROM dbo.Enrollment_Details
        INNER JOIN dbo.AthleticPrograms ON dbo.Enrollment_Details.ProgramID = dbo.AthleticPrograms.ProgramID
        INNER JOIN dbo.ProgramDivisions ON dbo.AthleticPrograms.ProgramID = dbo.ProgramDivisions.ProgramID
            AND dbo.Enrollment_Details.[Division Name] = dbo.ProgramDivisions.[Division Name]
        WHERE (dbo.Enrollment_Details.[Program Sort Order] > 0)
        GROUP BY dbo.AthleticPrograms.[Program Year],
                 dbo.AthleticPrograms.[Program Name],
                 dbo.AthleticPrograms.[Program Season],
                 dbo.AthleticPrograms.[Program Format],
                 dbo.AthleticPrograms.[Program Environment],
                 dbo.ProgramDivisions.[Division Name],
                 dbo.ProgramDivisions.[Division Gender]
        ORDER BY dbo.AthleticPrograms.[Program Year] DESC,
                 dbo.AthleticPrograms.[Program Name]
        """

        results = db.execute_query(query)
        return results
    except Exception as e:
        logger.error(f"Error fetching division stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/lifetime")
def get_lifetime_stats():
    """Get lifetime statistics for players and families"""
    try:
        players_query = "SELECT COUNT(DISTINCT [Player Id]) as PlayersLifetime FROM dbo.Enrollment_Details"
        families_query = "SELECT COUNT(DISTINCT [User Id]) as FamiliesLifetime FROM dbo.Enrollment_Details"

        players_result = db.execute_query(players_query)
        families_result = db.execute_query(families_query)

        return {
            "PlayersLifetime": players_result[0]["PlayersLifetime"] if players_result else 0,
            "FamiliesLifetime": families_result[0]["FamiliesLifetime"] if families_result else 0
        }
    except Exception as e:
        logger.error(f"Error fetching lifetime stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/yearly-breakdown")
def get_yearly_breakdown():
    """Get player and family counts for each year"""
    try:
        years = [2022, 2023, 2024, 2025]
        results = {}

        for year in years:
            players_query = f"""
            SELECT COUNT(DISTINCT [Player Id]) AS Players{year}
            FROM dbo.Enrollment_Details
            WHERE [Order Date] BETWEEN
                CONVERT(DATETIME, '{year}-01-01 00:00:00', 102) AND
                CONVERT(DATETIME, '{year}-12-31 00:00:00', 102)
            """

            families_query = f"""
            SELECT COUNT(DISTINCT [User Id]) AS Families{year}
            FROM dbo.Enrollment_Details
            WHERE [Order Date] BETWEEN
                CONVERT(DATETIME, '{year}-01-01 00:00:00', 102) AND
                CONVERT(DATETIME, '{year}-12-31 00:00:00', 102)
            """

            players_result = db.execute_query(players_query)
            families_result = db.execute_query(families_query)

            results[str(year)] = {
                "players": players_result[0][f"Players{year}"] if players_result else 0,
                "families": families_result[0][f"Families{year}"] if families_result else 0
            }

        return results
    except Exception as e:
        logger.error(f"Error fetching yearly breakdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/player-enrollments", response_model=List[PlayerEnrollmentStats])
def get_player_enrollment_stats(limit: int = 50):
    """Get top players by total program enrollments"""
    try:
        query = """
        SELECT TOP (?)
            e.[Player Id] as PlayerId,
            e.[Player First Name] as PlayerFirstName,
            e.[Player Last Name] as PlayerLastName,
            COUNT(DISTINCT e.ProgramID) as TotalEnrollments
        FROM dbo.Enrollment_Details e
        WHERE e.[Program Sort Order] > 0
        GROUP BY e.[Player Id], e.[Player First Name], e.[Player Last Name]
        ORDER BY COUNT(DISTINCT e.ProgramID) DESC, e.[Player Last Name], e.[Player First Name]
        """

        results = db.execute_query(query, (limit,))
        return results
    except Exception as e:
        logger.error(f"Error fetching player enrollment stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
