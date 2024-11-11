# FastAPI Secure Login & Admin API 🚀🔐

Welcome to my FastAPI Secure Login & Admin API project! 🎉 This began as a learning adventure in API security, packed with features like secure user authentication, rate limiting, and more crafted for anyone keen to understand and apply security principles in modern API development.

## 🛡️ Disclaimer 🛡️

This project was created for learning and demonstration purposes. While it follows best practices, certain configurations may be more advanced or simplified than needed in a production setting. **Use this as a foundation and adapt to your specific needs when building production-ready applications.** Also, note that this project is compatible with the following versions:

- **Pydantic:** 2.5.1
- **SQLAlchemy:** 2.0.23
- **FastAPI:** 0.104.1

## 📚 About This Project

This API combines essential security features JWT-based token authentication, rate limiting, and secure cookie handling to create a sturdy base for login and admin management. It’s designed as both a learning tool and a starting point for projects that need a solid foundation in API security. Some features may seem advanced for smaller projects, but they showcase patterns that are adaptable to real-world scenarios.

✨ *Think of this as a playground for learning, testing, and evolving API security skills. The goal here is secure functionality that can grow with you.* ✨

## 🌟 Core Features

- **FastAPI Power**: Fast and effective API development, nobody likes a slow server! 🏃‍♂️
- **OAuth 2.0 & JWTs**: Strong session security with access and refresh tokens stored in cookies for added protection 🔒
- **PostgreSQL Database**: Reliable and efficient data storage to back the API 📂
- **Rate Limiting**: Prevents abuse by capping requests, fully customizable to meet specific needs 🚦
- **SSL Ready**: Secure connections for production-readiness 🔐
- **Clean, Modular Code**: Built to be maintainable and extendable as needed 🧹

## 🚀 Quick Start

### 📋 Essentials

You’ll need the following to get started:

- **Python 3.11+**: For the latest features 🐍
- **PostgreSQL**: Our database of choice for storing user data 🗄️
- **Docker** (Optional): To make deployment a breeze 🐳

### ⚙️ Setup & Run

1. **Clone the Repository**:

   ```bash
   git clone https://github.com//CamiloCod3/Secure-Login-Admin-API.git
   cd SecureLogin_FastAPI
   ```

2. **Install Dependencies**:

   ```bash
   poetry install
   ```

3. **Set Up Environment**:
   Copy `.env.example` to `.env`, then add your secrets 🛠️

4. **Launch the Server**:

   ```bash
   uvicorn main:app --reload
   ```

5. **Optional Docker Deployment**:

   ```bash
   docker-compose up --build
   ```

## 🛡️ Security Features

This API is built with security at its core, showcasing techniques to protect data and enforce access controls:

- **Password Hashing**: Ensures passwords are stored securely 🔑
- **Token-based Auth**: Managed with JWT tokens for secure, verified access 🛂
- **SSL Configuration**: Keeps connections encrypted 🔐
- **Input Validation**: Blocks unwanted inputs, keeping the API secure and reliable 🛡️

### 🚀 Going Beyond: Production Considerations

For a production setting, consider adapting certain elements based on your needs:

- **Token Management**: A single access token might be sufficient for some use cases, or consider using providers like Auth0 or AWS Cognito 🔑
- **Dynamic Rate Limiting**: Tailor rate limits by user role or IP for better control 🕹️
- **API Gateway**: Offload tasks like rate limiting to a gateway (e.g., AWS API Gateway) to help with scalability and backend load 🚀

## 📄 License

Licensed under the **MIT License** use, learn, and build upon it!
