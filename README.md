# ☕ Vending Machine Application

A modern, full-stack vending machine application with a React frontend, FastAPI backend, and MySQL database. Features product categorization, real-time inventory management, and a smooth user experience with step-by-step purchasing flow.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI Backend│    │   MySQL Database │
│   (Vite + TS)   │◄──►│   (Python 3.13)  │◄──►│   (Docker)       │
│   Port: 3000    │    │   Port: 8000     │    │   Port: 3306     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technical Requirements

### System Requirements
- **Docker & Docker Compose**: Version 3.9+
- **Node.js**: 16+ (for local frontend development)
- **Python**: 3.13+ (for local backend development)
- **Git**: Latest version

### Hardware Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 2GB free space
- **CPU**: 2 cores minimum

## 📦 Dependencies & Libraries

### Backend (Python/FastAPI)
```
fastapi          # Web framework
uvicorn          # ASGI server
sqlalchemy       # ORM for database operations
pymysql          # MySQL driver
cryptography     # Security utilities
pytest           # Testing framework
httpx            # HTTP client for testing
```

### Frontend (React/Vite)
```
react            # UI framework (18.2.0)
react-dom        # React DOM rendering
axios            # HTTP client (1.13.2)
tailwindcss      # CSS framework (3.4.19)
vite             # Build tool (4.4.5)
react-hot-toast  # toast notification (2.6.0)
```

### Infrastructure
```
mysql:8.0        # Database
nginx:alpine     # Web server for production
node:16-alpine   # Build environment
python:3.13-slim # Runtime environment
```

## 🚀 Quick Start

### Option 1: Full Docker Deployment (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd vending-machine

# Build and run all services
docker compose up --build

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Database Admin: http://localhost:8080
```

### Option 2: Local Development

```bash
# Backend Setup
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend Setup (in another terminal)
cd vending-ui
npm install
npm run dev

# Database (via Docker)
docker run --name vending-db -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=vending -p 3306:3306 -d mysql:8.0
```

### Option 3: Hybrid Setup (Frontend Local, API in Docker)

```bash
# Start API and Database in Docker
docker compose up api db

# Start frontend locally
cd vending-ui
npm install
npm run dev

# Access points:
# Frontend: http://localhost:5173
# API: http://localhost:8000
```

## 📋 Setup Instructions

### 1. Environment Configuration

**⚠️ Important**: Environment files (`.env`) are NOT committed to Git for security reasons.

```bash
# Copy the example file and customize as needed
cd vending-ui
cp .env.example .env

# Edit .env with your specific configuration
# VITE_API_URL=http://localhost:8000  # For local development
# VITE_API_URL=http://api:8000        # For Docker deployment
```

**Environment Variables:**
- `VITE_API_URL`: Frontend API endpoint URL
  - Local development: `http://localhost:8000`
  - Docker deployment: `http://api:8000`

**Note**: The `.env` file is ignored by Git. Use `.env.example` as a template for required variables.

### 2. Database Initialization

The application automatically seeds the database with sample data on startup:

- **Products**: 10 sample products across categories (Drinks, Snacks, Nuts)
- **Money Stock**: THB denominations (1, 5, 10, 20, 50, 100 THB)

### 3. Build Process

```bash
# Full rebuild
docker compose down -v
docker compose up --build

# Clean rebuild (remove all containers and volumes)
docker compose down -v --remove-orphans
docker system prune -f
docker compose up --build
```

## 🔌 API Documentation

### Base URL
- **Production**: `http://localhost:8000`
- **Development**: `http://localhost:8000` or `http://api:8000` (in Docker)

### Authentication
No authentication required for vending operations.

### Product Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | List available products (stock > 0) |
| `GET` | `/products/all` | List all products (including out of stock) |
| `GET` | `/products/{id}` | Get specific product details |
| `POST` | `/products` | Create new product |
| `PUT` | `/products/{id}` | Update existing product |
| `DELETE` | `/products/{id}` | Delete product |

**Product Schema:**
```json
{
  "id": 1,
  "slot_no": "A1",
  "name": "Mineral Water",
  "price": 10,
  "stock": 50,
  "image_url": "https://..."
}
```

### Money Stock Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/money-stock` | List all money denominations |
| `POST` | `/money-stock` | Add new denomination |
| `PUT` | `/money-stock/{denom}` | Update stock quantity |
| `DELETE` | `/money-stock/{denom}` | Remove denomination |

**Money Stock Schema:**
```json
{
  "denom": 100,
  "quantity": 10,
  "type": "banknote"
}
```

### Vending Operations Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/select-product` | Select a product for purchase |
| `POST` | `/insert-money` | Insert money into machine |
| `POST` | `/confirm` | Confirm purchase and dispense |

**Vending Flow Example:**
```bash
# 1. Select product
curl -X POST http://localhost:8000/select-product \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'

# 2. Insert money
curl -X POST http://localhost:8000/insert-money \
  -H "Content-Type: application/json" \
  -d '{"session_id": "session-123", "denom": 10}'

# 3. Confirm purchase
curl -X POST http://localhost:8000/confirm \
  -H "Content-Type: application/json" \
  -d '{"session_id": "session-123"}'
```

## 🎨 Frontend Features

### User Interface
- **Responsive Design**: Works on desktop and mobile
- **Step-by-Step Flow**: Product selection → Payment → Success
- **Product Categories**: Drinks, Snacks, Nuts with emoji icons
- **Real-time Updates**: Live stock and money status
- **Accessibility**: Keyboard navigation and screen reader support

### Components
- `App.jsx` - Main application with state management
- `VendingScreen.jsx` - Product grid with categorization
- `ProductCard.jsx` - Individual product display
- `MoneyIcon.jsx` - Currency display with custom styling

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Colors**: Cafe-themed color palette
- **Animations**: Smooth transitions and hover effects
- **Icons**: Custom currency icons with CSS filters

## 🧪 Testing

### Backend Tests
```bash
cd api
pip install -r requirements.txt
pytest tests/ -v
```

### Frontend Tests
```bash
cd vending-ui
npm install
npm run lint
```

### Integration Tests
```bash
# Test API endpoints
python api/test_crud.py
```

## 🔧 Development

### Project Structure
```
vending-machine/
├── api/                    # FastAPI backend
│   ├── main.py            # Application entry point
│   ├── models.py          # SQLAlchemy models
│   ├── routers/           # API route handlers
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container
├── vending-ui/            # React frontend
│   ├── src/               # Source code
│   ├── package.json       # Node dependencies
│   ├── Dockerfile         # Frontend container
│   └── nginx.conf         # Nginx configuration
├── docker-compose.yml     # Multi-service orchestration
└── README.md             # This file
```

### Development Workflow
1. **Feature Branch**: Create feature branch from `main`
2. **Code Changes**: Make changes with proper testing
3. **Testing**: Run tests locally
4. **Docker Build**: Test with `docker compose up --build`
5. **Commit**: Commit with descriptive message
6. **Pull Request**: Create PR for review

### Environment Variables
- `VITE_API_URL`: Frontend API endpoint
- `DATABASE_URL`: Backend database connection
- `MYSQL_*`: Database configuration

## 🔒 Git Best Practices

### What NOT to Commit
- **Environment files** (`.env`) - Contain sensitive configuration
- **Secrets/API keys** - Never commit credentials
- **Large binary files** - Use Git LFS for assets >100MB
- **Build artifacts** - Generated files in `dist/`, `build/`
- **Dependencies** - `node_modules/`, virtual environments

### What SHOULD be Committed
- **Source code** - All `.js`, `.jsx`, `.py`, `.sql` files
- **Configuration templates** - `.env.example`, `config.example.json`
- **Documentation** - `README.md`, code comments
- **Build scripts** - `Dockerfile`, `docker-compose.yml`
- **Tests** - All test files and configurations

### Pre-commit Checklist
```bash
# Check for sensitive files
git status --ignored
git ls-files | grep -E '\.(env|key|pem)$'

# Verify .gitignore is working
echo "node_modules" >> .gitignore.test
git status --ignored | grep node_modules
rm .gitignore.test
```

