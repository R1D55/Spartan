# Chatbot Application

This repository contains the source code for a chatbot application built using Flask for the backend and Bootstrap for the frontend.

## Folder Structure

```plaintext
project-root/
│
├── app/
│   ├── __init__.py         # Initializes the Flask app
│   ├── routes.py           # Defines the routes for the chatbot
│   ├── chatbot.py          # Core logic for the chatbot
│   └── static/
│       └── css/            # Custom CSS files
│       └── js/             # JavaScript files
│   └── templates/
│       └── base.html       # Base HTML template for the project
│       └── chatbot.html    # HTML for the chatbot interface
│
├── tests/
│   ├── test_routes.py      # Unit tests for Flask routes
│   └── test_chatbot.py     # Unit tests for chatbot logic
│
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── run.py                  # Entry point for the application
```

## How to Run the Project

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/chatbot-application.git
cd chatbot-application
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to keep the dependencies isolated. You can create and activate a virtual environment using the following commands:

```bash
# For Linux/Mac
virtualenv venv
source venv/bin/activate

# For Windows
virtualenv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Set GEMINI API KEY

You will need to set your `GEMINI_API_KEY` environment variable for the application to function correctly. Use the following commands based on your operating system:

```bash
# For Linux/Mac
export GEMINI_API_KEY='your_api_key_here'

# For Windows
set GEMINI_API_KEY='your_api_key_here'
```

### 5. Run the Application

To start the Flask development server, run:

```bash
python run.py
```

The application should now be running at `http://127.0.0.1:5000/`. You can visit this URL in your browser to access the chatbot interface.
