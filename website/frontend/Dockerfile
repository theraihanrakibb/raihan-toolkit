# syntax=docker/dockerfile:1.6

# Stage 1 — build the React app with Vite
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2 — serve static files with nginx
FROM nginx:alpine

# Non-root: nginx already runs as nginx user by default in nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
