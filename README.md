# library-management-system
## Tech Stack
| Package     | Version |
|-------------|:-------:|
| Python      |  ≥ 3.9  |
| PyQt6       |  6.6.1  |
| bcrypt      |  4.1.2  |
| pyodbc      |  5.1.0  |
| matplotlib  |  3.8.2  |
| keyring     |         |
## Features Overview
### Authentication
- Login with username and password
- Auto-login on application start if "Remember me" is checked
- Forgot password and reset password dialog
- Registration form with validation (name, email, phone, DOB, gender, username, password)
### Member Management
- **Approved Members** tab
  - Display members information
  - Search member by name, email, phone
  - Edit member details (name, email, phone, role)
  - Delete member
- **Pending Members** tab
  - Display registration requests
  - Approve or reject registration requests
## System Requirements
- Windows OS
- Microsoft SQL Server (Express)
- Python 3.9 or higher
## Installation
### 1. Clone the repository (if using Git)
```
git clone <url>
cd library-management-system 
```
### 2. Install Python dependencies
```
pip install -r requirements.txt
```
### 3. Database setup


