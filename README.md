# 🛠️ GearGuard – The Ultimate Maintenance Tracker

A smart maintenance management system built with Django for the **Odoo Hackathon**. GearGuard helps organizations efficiently track assets and manage maintenance operations by providing a centralized platform that seamlessly connects Equipment, Maintenance Teams, and Service Requests.

The core goal is to improve asset reliability, reduce downtime, and give maintenance teams a clear, actionable view of their tasks.

## Team

- **Team Leader**: Krishna Viradiya - [@Kv1108](https://github.com/Kv1108)
- **Team Member**: Mahipal Chauhan - [@mahipal79](https://github.com/mahipal79)
- **Team Member**: Ravi Vyas - [@coderavi1612](https://github.com/coderavi1612)

## 🚀 Key Features & Modules

### 🔧 Equipment Management
Centralized database of all company assets (machines, vehicles, IT equipment).

**Capabilities:**
- Track equipment by department or assigned employee
- Store essential details:
  - Equipment name & serial number
  - Purchase date & warranty information
  - Physical location
  - Health status monitoring
- Assign default maintenance team and responsible technician
- Quick access to maintenance history via smart actions
- Advanced search and filtering by name or serial number

### 👷 Maintenance Teams
Support for multiple specialized maintenance teams reflecting real-world operations.

**Features:**
- Create teams (Mechanics, Electricians, IT Support, etc.)
- Assign technicians to specific teams
- Team-based request routing and access control
- Technician load visualization and utilization metrics

### 📝 Maintenance Requests
Core transactional module managing the full lifecycle of maintenance jobs.

**Request Types:**
- **Corrective Maintenance**: Unplanned repairs due to breakdowns
- **Preventive Maintenance**: Scheduled routine checkups

**Key Fields:**
- Issue subject (e.g., "Leaking Oil")
- Linked equipment or work center
- Scheduled date (for preventive tasks)
- Repair duration / hours spent
- Threaded comments and maintenance logs

### 🔄 Functional Workflows

**Flow 1: Breakdown Handling**
1. User creates a maintenance request
2. Selecting equipment auto-fills category and assigned team
3. Request starts in **New** status
4. Technician/manager assigns the request → **In Progress**
5. On completion, log duration and mark **Repaired**

**Flow 2: Preventive Maintenance**
1. Manager creates a preventive request
2. Schedule for specific date
3. Request appears in Calendar View
4. Helps teams prepare and avoid unexpected breakdowns

### 📊 User Interface & Views

**🗂️ Kanban Board**
- Primary workspace for technicians
- Stages: **New | In Progress | Repaired | Scrap**
- Drag-and-drop support for status updates
- Visual indicators:
  - Assigned technician avatars
  - Overdue requests highlighted with warning colors

**📅 Calendar View**
- Displays all preventive maintenance tasks
- Click on dates to quickly schedule new maintenance
- Improves planning and workload visibility

**📈 Intelligent Dashboard (V2)**
- Critical equipment tracking (health < 30%)
- Activity feed with recent maintenance actions
- Real-time team utilization metrics

### 🏭 Work Centers & Categories (V2)
- **Work Centers**: Manage production units with cost/hour, efficiency, and OEE metrics
- **Categories**: Organize assets (Robotics, Hydraulics, etc.) with responsible users
- **Dynamic Requests**: Toggle between Equipment and Work Center targets

### 🤖 Smart Automation & Advanced Features

**Smart Buttons**
- "Maintenance" button on equipment pages
- Shows all related maintenance requests
- Badge count of open requests

**Scrap Logic**
- Moving a request to **Scrap** automatically marks equipment as unusable
- Maintains accurate asset lifecycle records

**Auto-Fill Intelligence**
- Equipment selection auto-populates category and team
- Smart team assignment based on equipment definitions

### 🔐 Authentication System
- Secure login/signup with dedicated pages
- Separate accounts for technicians and managers
- Strict password validation (uppercase, lowercase, symbols, digits)
- Dark premium UI theme

## 🎯 Why GearGuard?

GearGuard goes beyond basic CRUD operations. With intelligent auto-fill logic, visual workflows, and real-world maintenance processes, it delivers an **Odoo-like experience** while remaining flexible and easy to extend.

**Key Differentiators:**
- Smart automation reduces manual data entry
- Visual Kanban workflow mirrors real maintenance operations
- Preventive maintenance calendar prevents unexpected breakdowns
- Team-based access control and workload management
- Comprehensive audit trail with maintenance logs

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

### For Technicians
1. **Login** with your credentials
2. **Kanban Board** shows your assigned maintenance requests
3. **Drag and drop** requests through workflow stages
4. **Log hours** and add comments on completed work
5. **Calendar** view for scheduled preventive maintenance

### For Managers
1. **Dashboard** provides overview of critical equipment and team load
2. **Create requests** for corrective or preventive maintenance
3. **Assign tasks** to appropriate teams and technicians
4. **Monitor progress** via Kanban board and activity feed
5. **Manage work centers** and equipment categories

### Core Workflows
- **Equipment Management**: Add and track assets with full maintenance history
- **Breakdown Handling**: Quick request creation with auto-filled team assignment
- **Preventive Scheduling**: Calendar-based planning to avoid downtime
- **Scrap Management**: Automatic equipment lifecycle tracking

## Contributing

This project was developed as part of a team effort. For contributions or issues, please contact the team members listed above.

