# Patient Management System

## Overview

The Patient Management System is a Django-based web application that enables healthcare users to manage patient records, record vital signs and access patient visit information.

## Backend Integration Approach

This project consumes the existing APIs provided in the supplied Postman collection. A separate backend API has not been developed for patient management.

The Django application communicates with the existing REST APIs to perform authentication, patient registration, retrieval of patient records, recording of vitals and management of patient visits.

**API Documentation:**  
https://documenter.getpostman.com/view/18832855/2sB3Wnx2PF


## Features

- User registration and authentication.
- Patient registration.
- View registered patients.
- View individual patient profiles.
- Record patient vital signs.
- Automatic BMI calculation.
- General health assessments.
- Overweight assessments.
- Retrieve patient visits by selected date.

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Taiwlind CSS
- REST API
- Requests

## API Endpoints Used

| Method | Endpoint | Description |
|---|---|---|
| POST | `user/signin` | User login |
| POST | `user/signup` | User registration |
| POST | `patients/register` | Register a patient |
| GET | `patients/view` | Retrieve patients |
| GET | `patients/show/{id}` | Retrieve patient details |
| POST | `vital/add` | Record patient vitals |
| POST | `visits/add` | Record patient assessments |
| POST | `visits/view` | Retrieve visits by date |

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd medicTrack
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the application

```bash
python manage.py runserver
```

Open your browser at:

`http://127.0.0.1:8000/`

## Security

- API access tokens are stored in Django sessions.
- Credentials and secret keys should not be committed to the repository.
- Patient information and database files should not be exposed publicly.

## Backend Architecture

The application uses Django as the web interface and integration layer, while patient data and related operations are handled by the existing external REST API.