FROM nginx:stable-alpine

WORKDIR /app

COPY . .
COPY nginx.conf /etc/nginx/conf.d/default.conf
