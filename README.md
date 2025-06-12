# Book-It Bookmark Manager 🔖

A modern, Flask-based bookmark manager web application with MongoDB backend and Docker support. Organize, search, and manage your favorite links with a clean, responsive interface.

## ✨ Features

- **📝 CRUD Operations**: Add, edit, delete, and view bookmarks
- **🔍 Smart Search**: Search bookmarks by name or URL
- **📂 Category Management**: Organize bookmarks with custom categories
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices
- **🎨 Modern UI**: Clean, intuitive interface with smooth animations
- **📄 Pagination**: Efficient browsing with paginated results
- **✅ URL Validation**: Ensures valid URLs are added
- **🔄 Real-time Updates**: Dynamic category suggestions
- **🐳 Docker Ready**: Easy deployment with Docker Compose
- **📊 Statistics**: View total bookmark counts and search results

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6
- **Containerization**: Docker & Docker Compose
- **Database Admin**: Mongo Express

## 📋 Prerequisites

- Docker and Docker Compose installed on your system
- Git (for cloning the repository)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/KingSajxxd/Book-It-Bookmark-Manager-Docker.git
cd Book-It-Bookmark-Manager-Docker
```

### 2. Environment Setup (Optional)

Copy the example environment file and modify if needed:

```bash
cp .env.example .env
```

# The application works out of the box with default settings, but you can customize:

```env
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=examplepassword
MONGO_EXPRESS_USER=root
MONGO_EXPRESS_PASSWORD=examplepassword
MONGO_URI=mongodb://root:examplepassword@mongo:27017/bookmarksdb
FLASK_ENV=development
```

### 3. Launch with Docker Compose

```bash
docker-compose up -d
```

### 4. Access the Application

- **Bookmark Manager**: http://localhost:5000
- **Mongo Express** (Database Admin): http://localhost:8081

## 📖 Usage Guide

### Adding Bookmarks

1. Click the **"Add New Bookmark"** button on the main page
2. Fill in the required fields:
   - **Name**: Display name for your bookmark
   - **URL**: Valid web address (required)
   - **Category**: Optional category for organization
   - **Description**: Optional description
3. Click **"Add Bookmark"** to save

### Managing Bookmarks

- **Edit**: Click the edit icon (✏️) on any bookmark card
- **Delete**: Click the delete icon (🗑️) and confirm
- **Visit**: Click the bookmark title to open the link in a new tab

### Searching

Use the search bar at the top to find bookmarks by:
- Bookmark name
- URL content

### Categories

- Categories are automatically suggested based on existing bookmarks
- Common categories include: Work, Personal, Entertainment, Education, News, Social
- Create custom categories by typing in the category field

## 🏗️ Project Structure

```
Book-It-Bookmark-Manager-Docker/
├── app/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── static/
│   │   └── style.css      # Application styles
│   └── templates/
│       ├── index.html     # Main page template
│       ├── edit.html      # Edit bookmark template
│       ├── 404.html       # 404 error page
│       └── 500.html       # 500 error page
├── docker-compose.yaml     # Docker services configuration
├── Dockerfile             # Application container setup
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## 🔧 Configuration

### Database Configuration

The application connects to MongoDB using these default settings:
- **Host**: mongo (Docker service name)
- **Port**: 27017
- **Database**: bookmarkdb
- **Collection**: bookmarks

### Flask Configuration

- **Host**: 0.0.0.0 (accessible from all interfaces)
- **Port**: 5000
- **Debug**: Disabled in production

## 🐳 Docker Services

### Web Service (Flask App)
- **Port**: 5000
- **Build**: Custom Dockerfile
- **Volumes**: ./logs:/app/logs (for log persistence)

### MongoDB Service
- **Port**: 27017
- **Image**: Official MongoDB
- **Volumes**: mongo-data:/data/db (data persistence)

### Mongo Express Service
- **Port**: 8081
- **Image**: Official Mongo Express
- **Purpose**: Database administration interface

## 🛡️ Error Handling

The application includes comprehensive error handling:

- **URL Validation**: Ensures valid URLs are added
- **Duplicate Prevention**: Checks for existing URLs
- **Database Errors**: Graceful handling of MongoDB connection issues
- **Custom Error Pages**: 404 and 500 error pages
- **Flash Messages**: User-friendly success/error notifications

## 🎨 UI Features

- **Responsive Design**: Mobile-first approach
- **Modern Styling**: CSS custom properties for consistent theming
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: Semantic HTML and proper contrast ratios
- **Flash Messages**: Auto-dismissing notification system

## 📱 Mobile Support

The application is fully responsive with:
- Collapsible navigation
- Touch-friendly buttons
- Optimized layouts for small screens
- Flexible grid system

## 🔍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main page with bookmarks list |
| POST | `/add` | Add new bookmark |
| GET | `/edit/<id>` | Edit bookmark form |
| POST | `/edit/<id>` | Update bookmark |
| GET | `/delete/<id>` | Delete bookmark |
| GET | `/categories` | Get all categories (JSON) |

## 🚦 Development

### Running Locally (without Docker)

1. Install Python dependencies:
```bash
cd app
pip install -r requirements.txt
```

2. Start MongoDB locally or update connection string

3. Run the Flask application:
```bash
python app.py
```

### Making Changes

1. Edit application files in the `app/` directory
2. Rebuild the Docker container:
```bash
docker-compose down
docker-compose up --build
```

## 📊 Database Schema

### Bookmark Document Structure

```javascript
{
  "_id": ObjectId,
  "name": String,
  "url": String,
  "category": String,
  "description": String,
  "created_at": DateTime,
  "updated_at": DateTime
}
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Container won't start:**
- Check if ports 5000, 27017, or 8081 are already in use
- Verify Docker and Docker Compose are properly installed

**Database connection failed:**
- Ensure MongoDB container is running: `docker-compose ps`
- Check container logs: `docker-compose logs mongo`

**Application errors:**
- Check application logs: `docker-compose logs web`
- Verify all required environment variables are set

### Logs Location

Application logs are stored in `./logs/` directory (mounted from container).


![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Latest-green?logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green?logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Supported-blue?logo=docker&logoColor=white)