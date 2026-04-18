Sports Team Match Review Web Application

A full‑stack web application designed for sports teams to upload, watch, and review match footage. The platform provides an easy‑to‑use interface for players, coaches, and managers to access recent match videos, leave feedback, and manage team information across multiple devices.

📌 Features

Match Video Retrieval  
- Users can view recent match footage from any device, with videos organised clearly for quick access.

Comment & Feedback System  
- Each match includes a comments section where players can leave constructive feedback to support team improvement.

Role‑Based Access Control
- Admin users (managers/coaches): upload and delete videos, manage users, oversee teams  
- Standard users (players): view matches, leave comments, browse teams and users

Multi‑Team Support  
- Designed for use across multiple teams within a competition or league.

Team & User Pages  
- View all registered teams and all users signed up to the platform.

🛠️ Tech Stack

Frontend
- Angular
- TypeScript
- HTML / SCSS

Backend
- Flask (Python)
- MongoDB
- REST API architecture

Other
- JWT / Auth0 (if used)
- Role‑based authentication
- Responsive design

📂 Project Structure

/SportsWebApp

   /frontend        → Angular client application  
   /backend         → Flask API + MongoDB integration  
   README.md

🚀 Running the Application

Backend (Flask)
- Navigate to the backend folder
- Install dependencies:  
     pip install -r requirements.txt
- Start the server:  
     python app.py

Frontend (Angular)  
- Navigate to the frontend folder
- Install dependencies:  
     npm install  
- Start the Angular app:  
     ng serve  

The frontend will typically run on http://localhost:4200 and the backend on http://localhost:5000.

🎯 Purpose of the Project   
The goal of this application is to provide a modern digital platform for sports teams to analyse performance, share feedback, and manage match footage efficiently. It demonstrates full‑stack development, user‑centred design, and practical implementation of authentication, video handling, and team‑based workflows.
