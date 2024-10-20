# COOKING-MAMA Setup Guide

COOKING-MAMA is a web application for kitchen inventory management. This guide will walk you through the process of setting up and running both the frontend and backend components of the application.

## Frontend Setup

The frontend of COOKING-MAMA is built using React and managed with pnpm.

### Prerequisites

1. Node.js (v14 or later recommended)
2. pnpm package manager

If you don't have pnpm installed, you can install it by following the instructions on the [official pnpm website](https://pnpm.io/installation).

### Steps

1. Open a terminal and navigate to the project root directory.

2. Change to the frontend directory:
   ```
   cd ./teamcook
   ```

3. Install dependencies using pnpm:
   ```
   pnpm i
   ```

4. Start the development server:
   ```
   npm start
   ```

The frontend application should now be running and accessible at `http://localhost:3000`.

## Backend Setup

The backend of COOKING-MAMA is built using Flask and requires a Python virtual environment.

### Prerequisites

1. Python 3.7 or later
2. pip (Python package installer)
3. virtualenv (recommended for creating isolated Python environments)

### Steps

1. Open a new terminal window and navigate to the project root directory.

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Create a new file named `.env` in the project root directory.
   - Add the following content to the `.env` file:

     ```
     # COOKING-MAMA Environment Variables

     # Flask application settings
     FLASK_APP=run.py
     FLASK_ENV=development

     # Secret key for session management and security
     # Replace this with a strong, random secret key in production
     SECRET_KEY=your_secret_key_here

     # Database connection URL
     # This example uses SQLite. For production, consider using a more robust database like PostgreSQL
     DATABASE_URL=sqlite:///app.db

     # Add any additional environment variables your application needs below
     ```

   - Replace `your_secret_key_here` with a strong, randomly generated secret key. You can generate one using Python:
     ```python
     import secrets
     print(secrets.token_hex(16))
     ```

6. Run database migrations:
   ```
   flask db upgrade
   ```

7. Start the Flask development server:
   ```
   flask run
   ```

The backend server should now be running and accessible at `http://127.0.0.1:5000`.

## Running the Application

With both frontend and backend servers running, you can now use the COOKING-MAMA application:

1. Open a web browser and go to `http://localhost:3000`
2. The frontend will communicate with the backend API at `http://127.0.0.1:5000`

## Important Notes

1. The `.env` file contains sensitive information and should never be committed to version control. Make sure it's listed in your `.gitignore` file.
2. For production environments, use a more secure database setup and ensure all sensitive information is properly protected.
3. The `SECRET_KEY` in the `.env` file should be kept secret and changed in production environments.
4. The `DATABASE_URL` provided uses SQLite, which is good for development but not recommended for production. For production, consider using PostgreSQL or another robust database system.

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are correctly installed
2. Check that you're in the correct directory when running commands
3. Verify that all environment variables are properly set in the `.env` file
4. Check the console output for any error messages

For more detailed information about the project structure, API endpoints, and component usage, please refer to the subsequent sections of this documentation.
