# COOKING-MAMA Setup Guide

COOKING-MAMA is a web application for kitchen inventory management. This guide will walk you through the process of setting up and running both the frontend and backend components of the application from scratch.

## Prerequisites

1. Git
2. Python 3.7 or later
3. Node.js (v14 or later recommended)
4. pnpm package manager
5. pip (Python package installer)

If you don't have pnpm installed, you can install it by following the instructions on the [official pnpm website](https://pnpm.io/installation).

## Initial Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/COOKING-MAMA.git
   cd COOKING-MAMA
   ```

## Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
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

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Populate the database with sample data:
   ```
   python populate_sample_data.py
   ```

7. Start the Flask development server:
   ```
   flask run
   ```

The backend server should now be running and accessible at `http://127.0.0.1:5000`.

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd teamcook
   ```

2. Install dependencies using pnpm:
   ```
   pnpm install
   ```

3. Start the development server:
   ```
   npm start
   ```

The frontend application should now be running and accessible at `http://localhost:3000`.

## Running the Application

With both frontend and backend servers running, you can now use the COOKING-MAMA application:

1. Open a web browser and go to `http://localhost:3000`
2. The frontend will communicate with the backend API at `http://127.0.0.1:5000`

## Important Notes

1. The `.env` file contains sensitive information and should never be committed to version control. Make sure it's listed in your `.gitignore` file.
2. For production environments, use a more secure database setup and ensure all sensitive information is properly protected.
3. The `SECRET_KEY` in the `.env` file should be kept secret and changed in production environments.
4. The `DATABASE_URL` provided uses SQLite, which is good for development but not recommended for production. For production, consider using PostgreSQL or another robust database system.
5. The `populate_sample_data.py` script is for development and testing purposes. In a production environment, you would have a different process for initializing your database.

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are correctly installed
2. Check that you're in the correct directory when running commands
3. Verify that all environment variables are properly set in the `.env` file
4. Check the console output for any error messages
5. If the database seems out of sync, try running `flask db upgrade` again, followed by `python populate_sample_data.py`

For more detailed information about the project structure, API endpoints, and component usage, please refer to the subsequent sections of this documentation.