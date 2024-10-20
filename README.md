# TeamCook: Kitchen Inventory Management System

TeamCook is a web application developed during a hackathon to address the challenges faced by kitchen teams in the food industry. It aims to streamline inventory management, improve team communication, and optimize budgeting for restaurants and professional kitchens.

## Important: Read the Project Documentation

For a comprehensive understanding of the project, including detailed user stories, feature specifications, and UI/UX designs, please read the `Project_Teamcook_PRD_TDD.pdf` file located in the root directory of this repository. This document provides crucial insights into the project's goals, features, and implementation details.

## Project Overview

### Vision
To revolutionize kitchen management by providing a comprehensive, user-friendly platform that enhances efficiency and reduces waste in professional kitchens.

### Key Features
- **Inventory System**: Real-time tracking of raw and processed ingredients
- **Recipe Book**: Centralized management of recipes with a drag-and-drop builder
- **Budgeting**: Cost tracking and financial analysis tools
- **Team Management**: Role-based access control for chiefs and cooks
- **Calendar Integration**: Scheduling and task management for kitchen teams

### Tech Stack
- Frontend: React with CoreUI
- Backend: Flask (Python)
- Database: SQLite (development) / PostgreSQL (production)
- API Integration: Toast POS API

## Setup Guide

### Prerequisites
1. Git
2. Python 3.7 or later
3. Node.js (v14 or later recommended)
4. pnpm package manager
5. pip (Python package installer)

If you don't have pnpm installed, follow the instructions on the [official pnpm website](https://pnpm.io/installation).

### Initial Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-repo/COOKING-MAMA.git
   cd COOKING-MAMA
   ```

### Backend Setup
1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root with the following content:
     ```
     FLASK_APP=run.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key_here
     DATABASE_URL=sqlite:///app.db
     ```
   - Replace `your_secret_key_here` with a generated key:
     ```python
     import secrets
     print(secrets.token_hex(16))
     ```

4. Initialize and populate the database:
   ```
   flask db upgrade
   python populate_sample_data.py
   ```

5. Start the Flask server:
   ```
   flask run
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd teamcook
   ```

2. Install dependencies and start the development server:
   ```
   pnpm install
   npm start
   ```

## Running the Application
- Backend: http://127.0.0.1:5000
- Frontend: http://localhost:3000

## Important Notes
- The `.env` file contains sensitive information and should not be committed to version control.
- For production, use a more secure database and protect sensitive information.
- The `populate_sample_data.py` script is for development purposes only.

## Troubleshooting
- Ensure all prerequisites are installed correctly.
- Verify environment variables in the `.env` file.
- Check console output for error messages.
- For database issues, try running `flask db upgrade` and `python populate_sample_data.py` again.

## Contributing
This project was developed during a hackathon by Oscar Chow, Zeth Tang, and Tat Chan. We welcome contributions and feedback to improve COOKING-MAMA!

## License
[Specify your license here]

For more detailed information about the project structure, API endpoints, and component usage, please refer to our documentation and the `Project_Teamcook_PRD_TDD.pdf` file in the root directory.
