# GearGuard

A premium maintenance management system built with Django, featuring robust authentication and an intelligent dashboard for tracking equipment health and maintenance operations.

## Team

- **Team Leader**: Krishna Viradiya - [@Kv1108](https://github.com/Kv1108)
- **Team Member**: Mahipal Chauhan - [@mahipal79](https://github.com/mahipal79)
- **Team Member**: Ravi Vyas - [@coderavi1612](https://github.com/coderavi1612)

## Features

### 1. Authentication System
- **Login/Signup**: Secure access with dedicated authentication pages
- **User Accounts**: Separate accounts for technicians and managers
- **Password Validation**: Strict requirements (uppercase, lowercase, symbols, digits)
- **Dark UI**: Consistent premium theme across all auth pages

### 2. Intelligent Dashboard (V2)
- **Critical Equipment Tracking**: Real-time monitoring of assets with health < 30%
- **Technician Load Visualization**: Team utilization metrics and insights
- **Activity Feed**: Quick view of recent maintenance actions and updates

### 3. Work Centers & Categories (V2)
- **Work Centers**: Manage production units with cost/hour, efficiency, and OEE metrics
- **Categories**: Organize assets (e.g., Robotics, Hydraulics) with assigned responsible users
- **Dynamic Requests**: Create maintenance requests for Equipment or Work Centers
- **Maintenance Logs**: Threaded comments and updates on every request

### 4. Equipment Management
- **Central Database**: Track all assets by department, owner, and assigned team
- **Smart Logic**: Auto-assigns teams based on equipment definitions
- **Advanced Search**: Filter equipment by name or serial number
- **Health Monitoring**: Track equipment condition and maintenance history

### 5. Maintenance Requests (Kanban Board)
- **Visual Workflow**: Drag and drop requests between stages:
  - New → In Progress → Repaired → Scrap
- **Auto-Save**: Status updates persist automatically
- **Scrap Logic**: Moving requests to "Scrap" automatically marks equipment as unusable

### 6. Preventive Maintenance (Calendar)
- **Monthly Schedule**: View and manage preventive maintenance tasks
- **Interactive Calendar**: Click on dates to schedule new maintenance checks
- **Task Integration**: Seamlessly integrated with equipment and work center data

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.x+
- SQLite (default) or PostgreSQL

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd gearguard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create admin user (optional):
```bash
python create_admin.py
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Access the application:
- Main App: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

### Default Credentials
- **Username**: admin
- **Password**: admin

## Project Structure

```
gearguard/
├── accounts/              # User authentication and account management
│   ├── templates/        # Login and signup pages
│   ├── validators.py     # Password validation logic
│   └── views.py          # Auth views
├── core/                 # Main application logic
│   ├── models.py         # Database models (Equipment, Team, Request, etc.)
│   ├── views.py          # Dashboard, Kanban, Calendar views
│   ├── forms.py          # Form definitions
│   ├── signals.py        # Automation logic (e.g., Scrap handling)
│   ├── templates/core/   # UI templates (HTML/CSS)
│   └── static/core/      # Static assets (CSS, JS)
├── gearguard/            # Project settings
│   ├── settings.py       # Django configuration
│   └── urls.py           # URL routing
└── manage.py             # Django management script
```

## V2 Verification

The system has been rigorously tested against V2 specifications:

- ✅ **Work Center Flow**: Creating process units with cost/efficiency metrics
- ✅ **Asset Management**: Assigning equipment to categories and work centers
- ✅ **Request Flexibility**: Toggle between equipment and work center targets
- ✅ **Security**: Strict password validation and secure authentication
- ✅ **Dynamic Forms**: Context-aware request creation
- ✅ **Maintenance Logs**: Threaded comment system

## Key Technologies

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Theme**: Dark premium design

## Usage

1. **Login** to the system with your credentials
2. **Dashboard** provides an overview of critical equipment and team load
3. **Equipment Management** to add and track assets
4. **Kanban Board** for visual maintenance workflow management
5. **Calendar** for scheduling preventive maintenance
6. **Work Centers** to manage production units and efficiency metrics

## Contributing

This project was developed as part of a team effort. For contributions or issues, please contact the team members listed above.

