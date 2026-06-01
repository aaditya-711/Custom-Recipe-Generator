# Custom Recipe Generator

An AI-powered recipe generator built using Flask and BoltIoT AI APIs.

Users can enter the ingredients available in their kitchen, and the application generates:
- A creative recipe name
- A funny recipe name
- Step-by-step cooking instructions
- A fun fact at the end

---

## Features

Clean and responsive UI
AI-generated recipes
Ingredient-based recipe generation
Copy-to-clipboard functionality
Flask backend
Real-time recipe generation

---

## Tech Stack

- Python
- Flask
- HTML/CSS
- JavaScript
- BoltIoT AI API

---

## Project Structure

```
project/
│
├── recipe_generator.py
├── README.md
├── .env
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Install dependencies

```bash
pip install flask
pip install boltiotai
```

### 3. Create a .env file

Create a file named `.env`

```env
BOLTIOT_API_KEY=your_api_key_here
```

### 4. Modify API key configuration

Replace:

```python
openai.api_key = "YOUR_API_KEY"
```

With:

```python
import os

openai.api_key = os.environ["BOLTIOT_API_KEY"]
```

### 5. Run the application

```bash
python app.py
```

Open:

```
http://localhost:8080
```

---

## Security Notice

This project requires a BoltIoT AI API key.

For security reasons, API keys are NOT included in this repository.

If you wish to run this project:

1. Obtain your own BoltIoT AI API key.
2. Create a `.env` file.
3. Add your API key as shown above.

Never commit API keys to GitHub.

---

## .gitignore

Add the following to your `.gitignore` file:

```gitignore
.env
__pycache__/
*.pyc
```

---

## Future Improvements

- Recipe images using AI image generation
- Download recipe as PDF
- Save favorite recipes
- User authentication
- Multiple cuisine options
- Nutrition information

---

## Author

Aaditya

Built as a learning project to explore:
- Flask
- AI APIs
- Frontend & Backend Integration
- Prompt Engineering