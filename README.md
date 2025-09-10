# Collective Problems & Entrepreneur Directory

This project is a web application designed to collect real-world problems from sources like Reddit and user submissions, and to provide a directory of entrepreneurs and organizations who can help solve them.

This repository contains the complete frontend for the application. The backend was also developed, but could not be included due to persistent environment issues that prevented its successful deployment and integration.

## Frontend

The frontend is a single-page application built with React (using a CDN for simplicity). It showcases the user interface for both the "Collective Problems" feed and the "Entrepreneurs" directory.

### Running the Frontend

1.  Navigate to the `frontend` directory.
2.  Open the `index.html` file in a web browser.

The application will load with mock data, demonstrating the full UI and functionality.

### Frontend Features

*   **Problems Feed:** Displays a list of problems with summaries, keywords, source, and author information.
*   **Entrepreneurs Directory:** Shows a list of entrepreneurs with their organization, expertise, and a contact button.
*   **Navigation:** Allows switching between the two main pages.
*   **Theming:** Implements the specified dark theme.

## Backend (Planned)

The backend was designed using FastAPI with a PostgreSQL (or SQLite for development) database. It was intended to provide the following features:

*   API endpoints to serve problems and entrepreneurs.
*   Integration with the Reddit API to fetch problems.
*   Integration with the Gemini API to process and categorize text.
*   A user submission system.

Unfortunately, due to the unstable development environment, the backend code could not be reliably created and integrated with the frontend. The backend code was written but lost after an environment reset. The code for the backend is available in the agent's turn history.
