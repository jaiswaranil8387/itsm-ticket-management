# Docker Setup Guide for Ticketing System

This guide explains how to run the Ticketing System using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

### 1. Development Mode (Single Container)
```bash
# Build and run the application
docker-compose up ticketing-app

# Or run in background
docker-compose up -d ticketing-app
```

### 2. Production Mode (With Nginx)
```bash
# Run with nginx reverse proxy
docker-compose --profile production up

# Or run in background
docker-compose --profile production up -d
```

## Services

### ticketing-app
- **Port**: 5000 (mapped to host port 5000)
- **Database**: SQLite stored in `./data/tickets.db`
- **Environment**: Production by default
- **Health Check**: Every 30 seconds

### nginx (production profile)
- **Port**: 80 (mapped to host port 80)
- **Purpose**: Reverse proxy with caching and security headers
- **Features**: Gzip compression, static file serving

## Useful Commands

### Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Logs and Monitoring
```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View specific service logs
docker-compose logs ticketing-app
docker-compose logs nginx
```

### Database Management
```bash
# Backup database
docker-compose exec ticketing-app cp /app/data/tickets.db /app/data/tickets.db.backup

# Access database
docker-compose exec ticketing-app python -c "
import sqlite3
conn = sqlite3.connect('/app/data/tickets.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM tickets')
print(cursor.fetchall())
conn.close()
"
```

### Health Checks
```bash
# Check if services are healthy
docker-compose ps

# Manual health check
curl http://localhost:5000/
curl http://localhost/health  # (production mode)
```

## Environment Variables

Copy `.env.example` to `.env` and modify as needed:
```bash
cp .env.example .env
```

## Volume Persistence

- `./data/` directory is mounted as `/app/data/` in the container
- Database file `tickets.db` is persisted across container restarts
- Static files are served directly by nginx in production mode

## Security Features

- Non-root user execution (UID 1000)
- Security headers in nginx configuration
- Health checks for service monitoring
- Restart policies for high availability

## Troubleshooting

### Port Already in Use
If port 5000 or 80 is already in use:
```bash
# Check what's using the port
netstat -tulpn | grep :5000

# Use different ports in docker-compose.yml
```

### Database Issues
```bash
# Reset database (WARNING: This will delete all data)
docker-compose down -v
docker-compose up
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R 1000:1000 ./data
```

## Development vs Production

### Development
- Direct access to Flask app on port 5000
- Debug mode enabled
- Hot reload available

### Production
- Nginx reverse proxy on port 80
- Static file caching
- Security headers
- Gzip compression
- SSL termination ready (add certificates to nginx.conf)
