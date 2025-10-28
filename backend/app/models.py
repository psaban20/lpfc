from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AthleticProgram(BaseModel):
    ProgramID: int
    ProgramName: Optional[str] = None
    ProgramSport: Optional[str] = None
    ProgramYear: Optional[int] = None
    ProgramSeason: Optional[str] = None
    ProgramFormat: Optional[str] = None
    ProgramEnvironment: Optional[str] = None
    ProgramSortOrder: Optional[int] = None

class ProgramDivision(BaseModel):
    DivisionID: int
    ProgramID: int
    DivisionName: Optional[str] = None
    DivisionFormat: Optional[str] = None
    DivisionGender: Optional[str] = None
    UpperDivision: Optional[str] = None
    LowerDivision: Optional[str] = None
    DivisionDuration_Weeks: Optional[int] = None
    DivisionPractices_PerWeek: Optional[int] = None
    DivisionPracticeLenth_Hours: Optional[float] = None
    DivisionGames_PerWeek: Optional[int] = None
    DivisionGameLength_Hours: Optional[float] = None

class EnrollmentDetail(BaseModel):
    ProgramName: Optional[str] = None
    DivisionName: Optional[str] = None
    AccountFirstName: Optional[str] = None
    AccountLastName: Optional[str] = None
    PlayerFirstName: Optional[str] = None
    PlayerLastName: Optional[str] = None
    PlayerGender: Optional[str] = None
    PlayerBirthDate: Optional[datetime] = None
    StreetAddress: Optional[str] = None
    Unit: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    PostalCode: Optional[str] = None
    UserEmail: Optional[str] = None
    Telephone: Optional[str] = None
    Cellphone: Optional[str] = None
    OtherPhone: Optional[str] = None
    TeamName: Optional[str] = None
    OrderDate: Optional[datetime] = None
    OrderNo: float
    OrderDetailDescription: Optional[str] = None
    OrderItemAmount: Optional[float] = None
    OrderItemAmountPaid: Optional[float] = None
    OrderItemBalance: Optional[float] = None
    OrderPaymentStatus: Optional[str] = None
    PlayerId: float
    UserId: float
    ProgramYear: Optional[int] = None
    ProgramSeason: Optional[str] = None
    ProgramSortOrder: Optional[int] = None
    DivisionGender: Optional[str] = None
    ProgramEnvironment: Optional[str] = None
    ProgramID: Optional[int] = None

class ProgramStats(BaseModel):
    ProgramName: str
    ProgramYear: int
    PlayerCount: int
    FamilyCount: int

class YearStats(BaseModel):
    ProgramYear: int
    UniquePlayerCount: int
    UniqueFamilyCount: int

class DivisionStats(BaseModel):
    ProgramYear: int
    ProgramName: str
    ProgramSeason: str
    ProgramFormat: str
    ProgramEnvironment: str
    DivisionName: str
    DivisionGender: str
    Players: int

class PlayerEnrollmentStats(BaseModel):
    PlayerId: int
    PlayerFirstName: str
    PlayerLastName: str
    TotalEnrollments: int
