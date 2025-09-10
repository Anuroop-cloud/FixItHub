# Collective Problems & Entrepreneur Directory

This project is a full-stack web application designed to collect real-world problems and connect them with entrepreneurs.

## Running the Application

To run this application, you will need to start both the backend server and the frontend.

### 1. Backend Setup

The backend is a FastAPI application.

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables (Optional):**
    The backend is pre-configured to run with a local SQLite database. For features like fetching data from Reddit or using the Gemini API, you would need to create a `.env` file in the `backend` directory with the following content:
    ```
    REDDIT_CLIENT_ID="your_client_id"
    REDDIT_CLIENT_SECRET="your_client_secret"
    REDDIT_USER_AGENT="your_user_agent"
    GEMINI_API_KEY="your_gemini_api_key"
    ```

4.  **Run the Backend Server:**
    From the root directory of the project, run:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend API will be available at `http://localhost:8000`. The server will start with some pre-populated dummy data.

### 2. Frontend Setup

The frontend is a React application.

1.  **Open the Frontend:**
    Navigate to the `frontend` directory and open the `index.html` file in a modern web browser.

2.  **View the Application:**
    The application will connect to the running backend server and display the problems and entrepreneurs. You can switch between the two views using the navigation buttons.

## Project Structure

*   `/backend`: Contains the FastAPI application, database models, and API logic.
*   `/frontend`: Contains the React single-page application.
*   `README.md`: This file.
