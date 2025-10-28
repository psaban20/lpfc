# LPFC Athletic Programs Dashboard

A full-stack application for managing and visualizing athletic program enrollments with a FastAPI backend and Next.js frontend, dockerized for easy deployment on Windows using Docker Desktop.

## Features

- **FastAPI Backend**: RESTful API with comprehensive endpoints for programs, divisions, enrollments, and statistics
- **Next.js Frontend**: Modern, responsive dashboard with beautiful tables and interactive charts
- **Azure SQL Server Integration**: Direct connection to your Azure SQL database
- **Dockerized**: Complete Docker setup for both backend and frontend
- **Real-time Statistics**: View enrollment trends, program statistics, and division breakdowns
- **Interactive Charts**: Visualize data with bar charts, line charts, and statistical cards

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- pyodbc (Azure SQL Server driver)
- Pydantic for data validation
- Uvicorn ASGI server

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Recharts for data visualization
- Axios for API calls

## Project Structure

```
lpfc/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # Database connection
│   │   └── models.py        # Pydantic models
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main dashboard page
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── lib/
│   │   └── api.ts           # API client functions
│   ├── Dockerfile
│   ├── package.json
│   └── .env.local
├── docker-compose.yml
├── .env
└── README.md
```

## Prerequisites

- Docker Desktop for Windows installed and running
- Git (optional, for cloning)

## Setup Instructions

### 1. Configure Environment Variables

The `.env` file has already been created with your database credentials:

```env
DB_PASSWORD=!Jenn1980
```

**IMPORTANT**: The `.env` file contains sensitive information. Make sure to add it to `.gitignore` if committing to git.

### 2. Build and Run with Docker

Open a terminal in the project root directory and run:

```bash
docker-compose up --build
```

This command will:
- Build the backend Docker image with Python and SQL Server ODBC drivers
- Build the frontend Docker image with Node.js
- Start both containers
- Backend will be available at `http://localhost:8000`
- Frontend will be available at `http://localhost:3000`

### 3. Access the Application

- **Frontend Dashboard**: Open your browser and navigate to `http://localhost:3000`
- **Backend API Docs**: View the interactive API documentation at `http://localhost:8000/docs`
- **Backend Health Check**: `http://localhost:8000/health`

## API Endpoints

### Programs
- `GET /programs` - Get all athletic programs
- `GET /programs?year={year}` - Filter programs by year
- `GET /programs/{program_id}` - Get specific program

### Divisions
- `GET /divisions` - Get all program divisions
- `GET /divisions?program_id={id}` - Filter divisions by program

### Enrollments
- `GET /enrollments` - Get enrollment details
- `GET /enrollments?program_id={id}&year={year}&limit={n}` - Filter enrollments

### Statistics
- `GET /stats/programs` - Player and family counts by program
- `GET /stats/years` - Player and family counts by year
- `GET /stats/divisions` - Player counts by division
- `GET /stats/lifetime` - Lifetime player and family totals
- `GET /stats/yearly-breakdown` - Breakdown by specific years (2022-2025)

## Dashboard Features

The frontend dashboard includes:

1. **Overview Cards**: Display key metrics
   - Total Players (Lifetime)
   - Total Families (Lifetime)
   - Number of Programs
   - Active Years

2. **Yearly Trends Chart**: Line chart showing player and family growth over time

3. **Players by Year Chart**: Bar chart comparing players and families by year

4. **Program Enrollment Chart**: Horizontal bar chart showing enrollment by program

5. **Division Statistics Table**: Detailed breakdown of players by division, program, and gender

6. **Recent Enrollments Table**: Latest enrollments with player info and payment status

## Database Schema

The application connects to the following tables:

- **AthleticPrograms**: Sports programs with year, season, format
- **ProgramDivisions**: Divisions within programs (age groups, skill levels)
- **Enrollment_Details**: Player enrollments with contact and payment info

## Development

### Running Locally Without Docker

#### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Stopping the Containers

```bash
docker-compose down
```

### Rebuilding After Changes

```bash
docker-compose up --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## Troubleshooting

### Backend Connection Issues

1. Check if Docker containers are running:
   ```bash
   docker ps
   ```

2. Verify database credentials in `.env` file

3. Check backend logs:
   ```bash
   docker-compose logs backend
   ```

4. Test database connection:
   ```bash
   curl http://localhost:8000/health
   ```

### Frontend Not Loading Data

1. Ensure backend is running and healthy
2. Check browser console for errors
3. Verify API URL in frontend `.env.local` file
4. Check frontend logs:
   ```bash
   docker-compose logs frontend
   ```

### Port Conflicts

If ports 3000 or 8000 are already in use:
1. Stop other services using those ports
2. Or modify ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "8001:8000"  # Change 8000 to 8001
   ```

## Database Connection Details

- **Host**: lpfc.database.windows.net
- **Database**: LPFC-DB
- **User**: appuser@lpfc.database.windows.net
- **Driver**: ODBC Driver 18 for SQL Server

## Security Notes

- The `.env` file contains sensitive credentials and should never be committed to version control
- In production, use environment variables or secure secret management
- Consider implementing authentication and authorization for the API
- Use HTTPS in production environments
- Update CORS settings in production to allow only specific origins

## Future Enhancements

- User authentication and role-based access control
- Export data to CSV/Excel
- Advanced filtering and search capabilities
- Email notifications for new enrollments
- Payment processing integration
- Mobile responsive optimizations
- Dark mode support

## License

This project is proprietary and confidential.

## Support

For issues or questions, please contact the development team.
