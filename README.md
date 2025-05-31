# Chad Store

Welcome to Chad Store! This is an e-commerce backend project I built specifically with **Mziuri students** to help students master modern web development with Django and REST APIs.

### Core Features
- **User Management**: Complete authentication system with sign up, email verification, login, and password reset functionality
- **Product Catalog**: Browse products and categories with proper image handling, filters, pagination  
- **Shopping Features**: Add items to cart and mark favorites for a complete shopping experience
- **Admin Powers**: Admin panel where admins can add new products and manage categories
- **API Documentation**: Interactive Swagger documentation 
- **Background Jobs**: Asynchronous email sending

## Tech Stack

This project uses industry-standard tools that you'll encounter in professional development:

| Technology | Purpose |
|------------|---------|
| **Django + DRF** | Web framework and REST API development |
| **PostgreSQL** | Production-ready relational database |
| **Redis** | High-performance caching and task queue management |
| **Celery** | Distributed background task processing |
| **Docker** | Containerization for consistent deployment |
| **JWT** | Secure, stateless authentication |
| **Swagger** | Auto-generated interactive API documentation |

## Getting Started

Follow these steps to get Chad Store running on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/fantozy/chad.store.git
cd chad.store
```

### 2. Set Up Environment Variables
```bash
touch .env
nano .env
```
Fill in your `.env` file following the template provided in `.env.example` from the repository. This includes database credentials, email settings, and secret keys.

### 3. Launch the Application
```bash
docker-compose up --build
```
This command will build and start all necessary containers. Wait for all services to initialize completely.

### 4. Verify Installation
Check that all containers are running properly:
```bash
docker ps
```
You should see **4 containers** running:
- `web` - Django application
- `db` - PostgreSQL database  
- `redis` - Redis cache server
- `celery` - Background task worker

### 5. Configure the Project
Access the web container and set up the database:
```bash
docker exec -it <web-container-id> bash
python manage.py migrate
python manage.py createproducts
python manage.py test
```

**Pro tip**: Use `docker ps` to find your exact web container ID, or use `docker exec -it chadstore-web-1 bash` if that's your container name.

### 6. Start Exploring!

Your Chad Store is now ready! Here's what you can access:

- **API Documentation**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API Base URL**: [http://localhost:8000/api/](http://localhost:8000/api/)

## 🔧 Development Tips

- Use the Swagger interface to test API endpoints interactively
- Check container logs with `docker-compose logs <service-name>` if you encounter issues
- The `creat_eproducts` command populates your database with sample data for testing
- All tests should pass - if they don't, check your environment configuration
