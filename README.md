# SolvingProblemsWithProgramming
test

## Document Tracker

### 1. Which aspects of the problem can potentially be solved with a program
The program can solve the problems of tracking, accessing, and managing physical files. It automates file check-out, return, and handover processes, records usage history, and enforces role-based access control to secure storage. It also reduces manual paperwork and human errors by maintaining a structured digital record of all file movements.

### 2. How solving the problem with a program changes the original process
The manual, paper-based tracking of files becomes a digital and automated system. Instead of writing in logbooks, users now perform actions (register, borrow, return, handover) through an online dashboard. File history is automatically recorded, reducing administrative workload and increasing transparency and accountability.

### 3. What requirements solving the problem places on the program
The program must:

- Support multiple user roles (admin, secretary, regular user).
- Maintain secure login and session handling.
- Provide file registration, checkout, return, and handover functions.
- Store data persistently and reliably (initially using a JSON file).
- Handle access restrictions for secured cupboards.
- Keep a detailed history of all actions for audit purposes.
- Offer a clear, user-friendly interface for non-technical users.

### 4. How using the program to solve the problem changes the original operating model
The operating model changes from a decentralized, manual file management process to a centralized, role-based digital system. Each user’s actions are logged, permissions are enforced automatically, and the administrator gains full visibility over file activity. The process becomes faster, more secure, and easier to audit.

### 5. In what kinds of situations the program will be used
The program will be used in offices, schools, and organizations that manage physical files or archives. It is suitable for environments where multiple users need to borrow, return, or register files while maintaining proper accountability and access control.

### 6. What requirements these situations place on the program
The program should run on an internal or local web server accessible through a browser. It must handle multiple users safely via sessions and ensure data integrity when files are checked out or returned simultaneously. A simple server (e.g., Flask’s built-in or a local intranet deployment) is sufficient for small-scale use.

### 7. What kind of software architecture you are planning for the program and why
The system uses a three-layer architecture:

- Presentation layer: HTML templates rendered by Flask (Jinja2).
- Application layer: Flask routes and logic for authentication, access control, and file operations.
- Data layer: JSON file storing users, cupboards, drawers, and file histories.

This architecture is chosen for simplicity, modularity, and ease of later upgrading to a database system.

### 8. How the correct functioning of the program can be ensured
Correct functioning is ensured by:

- Input validation and error handling (missing files, permissions, etc.).
- Testing key functions (login, checkout, return, and registration).
- Keeping consistent data through atomic read/write operations.
- Logging all actions in each file’s history for transparency and auditing.

### 9. What usability aspects you have considered
The interface is simple and role-specific. Users see only the cupboards they are allowed to access. Flash messages confirm success or errors after each action. The design minimizes clicks and input fields, guiding users step-by-step through file operations.

### 10. How the program should be used
Users log in with their credentials, view available cupboards and files, and perform actions such as registering, checking out, returning, or handing over files. Each action is automatically saved in the file’s history. Administrators can view all files, monitor activity, and manage secured storage areas. Users should log out after completing their tasks.
