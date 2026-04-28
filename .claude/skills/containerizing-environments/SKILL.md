---
name: containerizing-environments
description: This skill should be used when the user asks to "write a Dockerfile", "set up docker-compose", "containerize an app", "optimize Docker image size", "multi-stage build", "Docker networking", "Docker volumes", or discusses "container", "Docker Compose", "Alpine", "dev container", "environment consistency", "CI/CD container", or "deployment pipeline". Unifies Docker core commands, Dockerfile optimization, Compose orchestration, and production deployment patterns into a complete container workflow.
version: 1.0.0
---

# Docker DevOps

## Purpose

Unified Docker + Compose guide solving environment consistency and deployment complexity. Merges docker-essentials (core commands) with docker-compose (multi-container orchestration) for a complete container workflow.

## When to Use

Auto-activates when:
- Writing Dockerfiles
- Designing docker-compose.yml
- Debugging container networking or volume issues
- Setting up multi-service development environments
- Optimizing image size or build time
- Planning CI/CD container pipelines

## Core Patterns

### 1. Dockerfile Best Practices
```dockerfile
# Multi-stage build: separate build → runtime
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Optimization Rules:**
- **Order layers by change frequency**: dependencies → config → code
- **Use Alpine/slim** base images (reduce attack surface)
- **Combine RUN** commands (`&& \`) to minimize layers
- **`.dockerignore`**: exclude node_modules, .git, .env, test files
- **Specific tags** over `latest` (`node:20-alpine` not `node:latest`)

### 2. Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ['3000:3000']
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/app
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app

  redis:
    image: redis:7-alpine
    ports: ['6379:6379']

volumes:
  pgdata:
```

### 3. Essential Commands
```bash
# Development
docker compose up -d                    # Start all services
docker compose up -d --build app        # Rebuild and start specific service
docker compose logs -f app              # Follow specific service logs
docker compose exec app sh              # Shell into container

# Management
docker system prune -af --volumes       # Clean everything
docker stats                            # Live resource usage
docker compose down -v                  # Stop + remove volumes
```

### Resource Files
- [Container Security](resources/container-security.md) — non-root users, secrets, scanning, network policies
- [Production Deployment](resources/production-deploy.md) — orchestration (k8s), health checks, logging drivers, resource limits
