# Event Management System - Setup Guide

## New Features Added

✅ **2. User Authentication (JWT)**
- Secure login system with role-based access control
- Three default roles: Admin, Manager, Viewer
- Token-based authentication

✅ **3. Historical Analytics & Reporting**
- Database persistence for all zone metrics
- Historical data tracking and analysis
- Aggregated reports by time periods
- Audit logging for user actions

✅ **6. Alerting/Notification System**
- Automatic alerts for bottlenecks and high density
- Configurable severity thresholds (medium, high, critical)
- Real-time alert notifications in dashboard
- Alert management and tracking

✅ **7. Secure API Key Management**
- Environment variables for sensitive configuration
- No hardcoded credentials
- Secure .env file setup

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit `.env` file with your actual values:

```env
# OpenAI/xAI API Configuration
XAI_API_KEY=your_actual_api_key_here

# JWT Authentication (generate a strong secret key)
JWT_SECRET_KEY=your_super_secret_key_here_change_this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./event_management.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 3. Install Dashboard Dependencies

```bash
cd dashboard
npm install
cd ..
```

### 4. Start the Backend Server

```bash
uvicorn data_engine:app --reload
```

The server will start at `http://localhost:8000`

### 5. Start the Dashboard

In a new terminal:

```bash
cd dashboard
npm run dev
```

The dashboard will start at `http://localhost:5173`

## Default User Credentials

| Username | Password    | Role    | Permissions                    |
|----------|-------------|---------|--------------------------------|
| admin    | admin123    | Admin   | Full access, user management   |
| manager  | manager123  | Manager | View analytics and alerts      |
| viewer   | viewer123   | Viewer  | View-only dashboard access     |

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/register` - Register new user (admin only)

### Analytics & Reporting
- `GET /api/analytics/zones/history` - Get historical zone data
- `GET /api/analytics/zones/report` - Generate aggregated reports
- `GET /api/analytics/alerts/summary` - Get alert statistics
- `GET /api/analytics/alerts` - Get list of alerts
- `POST /api/analytics/alerts/{alert_id}/read` - Mark alert as read
- `GET /api/analytics/audit-logs` - Get audit logs (admin/manager)

### Alerts
- `GET /api/alerts/thresholds` - Get alert threshold configuration
- `GET /api/alerts/unread-count` - Get count of unread alerts
- `GET /api/alerts/recent` - Get recent alerts

### Event Data
- `GET /api/zones` - Get current zone status
- `GET /api/recommendations` - Get best routing recommendations

## Database

The system automatically creates an SQLite database (`event_management.db`) with the following tables:

- **zone_snapshots** - Historical zone metrics (updated every 5 seconds)
- **alerts** - Alert records with severity and status
- **audit_logs** - User action audit trail

## Security Notes

⚠️ **Important for Production:**
1. Change the `JWT_SECRET_KEY` to a strong, random string
2. Use a production database (PostgreSQL/MySQL) instead of SQLite
3. Enable HTTPS
4. Implement rate limiting
5. Change default user passwords
6. Use environment-specific .env files
7. Never commit .env files to version control

## Testing the Features

### Test Authentication:
1. Open dashboard at `http://localhost:5173`
2. Login with default credentials
3. Verify token is stored in localStorage
4. Try accessing protected endpoints

### Test Alerts:
1. Wait for the simulation to generate high density zones
2. Check the bell icon in the dashboard header
3. Click to view alerts
4. Click on unread alerts to mark them as read

### Test Analytics:
1. Let the system run for a few minutes to collect data
2. Use the API endpoints to fetch historical data
3. Generate reports for different time periods
4. Check audit logs for user actions

## Troubleshooting

### Database Issues:
- Delete `event_management.db` and restart the server to reset
- Check SQLAlchemy logs for connection errors

### Authentication Issues:
- Verify JWT_SECRET_KEY is set in .env
- Check token expiration settings
- Clear localStorage and login again

### Alert Issues:
- Check alert thresholds in alerts.py
- Verify database is being written to
- Check browser console for errors

## Next Steps

To further enhance the system:
- Integrate real IoT sensors for actual crowd data
- Add email/SMS notifications for critical alerts
- Implement WebSocket for real-time updates
- Add data visualization charts
- Create mobile app for attendees
- Add staff scheduling module
