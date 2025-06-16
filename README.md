# PyMeet - Google Meet Clone

PyMeet is a video meeting application inspired by Google Meet, built using FastAPI, SQLite, HTML/CSS/JavaScript, and WebRTC. It allows users to create and join video meetings in real-time.

## Features

* **User Authentication:** Login and registration functionality with JWT authentication.
* **Meeting Creation and Joining:** Users can create new meetings or join existing ones.
* **Real-time Video Chat:** Integrated WebRTC for real-time video and audio communication.
* **Chat and Signaling:** Real-time chat functionality for meeting participants.
* **Responsive UI:** Designed with HTML templates for a user-friendly experience across devices.

## Project Structure

The project is structured as follows:

* **app/**: Contains the FastAPI application and its components.

  * **main.py**: Entry point for the FastAPI application.
  * **routers/**: API routes for authentication, meeting management, and WebSocket signaling.
  * **models/**: SQLAlchemy models for database interactions.
  * **db/**: Database setup using SQLite.
  * **utils/**: Utility functions for JWT handling and WebRTC signaling.
  * **templates/**: HTML templates for user interfaces (login, dashboard, meeting).
* **static/**: Static assets such as CSS stylesheets and JavaScript files.
* **.env**: Environment variables including JWT\_SECRET and other sensitive data.
* **requirements.txt**: Dependencies required to run the application.

## Installation

1. Clone the repository:

   ```
  [ git clone https://github.com/yourusername/pymeet.git](https://github.com/sanskratipatel/PyMeet-Google-Meet-Clone.git)
   cd pymeet
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory with the following:

   ```
   JWT_SECRET=your_jwt_secret_key
   ```

4. Run the application:

   ```
   uvicorn app.main:app --reload
   ```

   This command starts the FastAPI server with automatic reloading on code changes.

5. Access the application:

   Open a web browser and go to `http://localhost:8000` to access the PyMeet application.

## Contributing

Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
* **WebRTC**: A free, open-source project that provides browsers and mobile applications with Real-Time Communications (RTC) capabilities via simple APIs.

