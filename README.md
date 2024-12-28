# EchoAnswer
 This is a tool which uses the power of AI to answer your questions based on context
# EchoAnswer

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Overview](#project-overview)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Database Models](#database-models)
6. [Folder Structure](#folder-structure)

---

## Getting Started

### Prerequisites

Before cloning and running the project, ensure you have the following installed:

- Python 3.9 or higher
- Django 5.1
- PostgreSQL
- Node.js (for managing frontend assets if needed)
- pip and virtualenv

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/EchoAnswer.git
   cd EchoAnswer
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate  # Windows
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the PostgreSQL database:
   - Create a database in PostgreSQL (e.g., `echoanswer_db`).
   - Update the `DATABASES` section in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'echoanswer_db',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': '127.0.0.1',
             'PORT': '5432',
         }
     }
     ```

5. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at:
   - `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

---

## Project Overview

### Objective

EchoAnswer is a **context-aware chatbot** system designed to provide users with intelligent, context-driven conversational capabilities. It integrates advanced **natural language processing** with a scalable **Django backend**.

### Key Functionalities

- Multi-format **context input**: Text, URLs, files, and audio.
- User **authentication and profile management**.
- Personalized **chat history and usage analytics**.
- Responsive **frontend interface** built with Bootstrap.

---

## Features

### User Features

- **Signup/Login**: Secure user authentication.
- **Profile Management**: Update details and profile picture.
- **Chat History**: View user-specific previous chats.
- **Usage Statistics**: Visual analytics for daily chat activity.

### Chat Features

- **Context-Aware Responses**: Users can input context in the following formats:
  - **Text Paragraphs**
  - **URLs**
  - **PDF Files**
  - **Audio Transcriptions**
- **Dynamic Chat Updates**: Real-time responses based on user input.

### Admin Features

- Full control over user profiles and chat data.
- Ability to delete or modify user data.

---

## Technologies Used

### Backend

- **Python**
- **Django Framework**
- **PostgreSQL** (Database)
- **Transformers Library**: For NLP and question-answering capabilities.

### Frontend

- **HTML5/CSS3**
- **JavaScript** (ES6+)
- **Bootstrap 5**: For responsive design.
- **Chart.js**: For dynamic usage statistics visualization.

### Others

- **File Handling**: Handles media uploads for profile pictures and file-based context inputs.
- **Django Signals**: Used to automatically create user profiles.

---

## Database Models

### User
- Built-in Django `User` model used for authentication.

### Profile
| Field            | Type            | Description                           |
|------------------|-----------------|---------------------------------------|
| `user`           | OneToOneField   | Links to the User model.             |
| `profile_picture`| ImageField      | Stores the user's profile picture.   |
| `location`       | CharField       | Optional location field.             |
| `occupation`     | CharField       | Optional occupation field.           |

### Chat
| Field        | Type           | Description                           |
|--------------|----------------|---------------------------------------|
| `user`       | ForeignKey     | Links to the User model.             |
| `user_input` | TextField      | Stores user input.                   |
| `bot_response`| TextField     | Stores chatbot responses.            |
| `context`    | TextField      | Stores context for the chat.         |
| `created_at` | DateTimeField  | Auto-generated timestamp.            |

---

## Folder Structure

```plaintext
EchoAnswer/
├── chat/                      # App folder
│   ├── migrations/            # Migration files
│   ├── static/                # Static files (CSS, JS, assets)
│   ├── templates/             # HTML templates
│   ├── views.py               # App views
│   ├── models.py              # App models
│   ├── urls.py                # App URLs
├── media/                     # Media files (e.g., profile pictures)
├── static/                    # Global static files
├── templates/                 # Global templates
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## How to Contribute

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For further details or questions, please contact [Your Name](mailto:your.email@example.com).
