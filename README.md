---

# FastAPI Secure Login: A DevSecOps Adventure 🚀🔐

Embarking on a quest through the realms of DevSecOps and backend development, I've crafted a secure login system that's not just a piece of software but a testament to my journey. Utilizing FastAPI, this project is a blend of modern security practices, a sprinkle of async magic, and a whole lot of learning. It's where OAuth meets JWTs, all in the pursuit of mastering secure user authentication and having a blast along the way!

## Core Features

- **FastAPI at Heart**: Speed and simplicity, because who likes waiting?
- **OAuth 2.0 & JWTs**: Like a fortress guarding precious treasures (aka user sessions).
- **PostgreSQL**: Sturdy as a rock, for all our data-keeping needs.
- **Asynchronous Magic**: Making our app swift and responsive, because performance is key.
- **SSL Ready**: Because we like our connections like we like our secrets — secure.
- **Clean Code Club**: Modular, maintainable, and merry!

## Quick Start

### Essentials

- **Python 3.8+**: The more, the merrier.
- **PostgreSQL**: Our data haven.
- **Docker** (Optional): Containers make life easier.
- **Poetry**: Dependency management but make it poetic.

### Setup & Run

1. **Grab the Code**:
  ```bash
  git clone https://github.com/yourusername/SecureLogin_FastAPI.git
  ```
  ```bash
  cd SecureLogin_FastAPI
  ```
  
2. **Install Dependencies**:
  ```bash  
  poetry install
  ```
3. **Enviro-Setup**:
   Peek at `.env.example`, then set your own secrets.

### Fire It Up

- **Server Time**:
  ```bash
  uvicorn main:app --reload
  ```
- **Swagger Time**:
  Head over to `http://localhost:8000/docs` and start playing.

### Docker Route (Optional)

- **Compose It**:
  ```bash
  docker-compose up --build
  ``` 

## On Security

A playground for security goodies:
- **Password Hashing**: Keeping secrets safe.
- **Token-based Auth**: Access granted, the secure way.
- **SSL Config**: Encrypted conversations only.
- **Input Validation**: No unwelcome guests here!


Licensed for fun under [MIT License](LICENSE)
