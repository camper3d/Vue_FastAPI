FROM node:18 AS build

WORKDIR /app

COPY vue_tasks/package*.json ./
RUN npm install

COPY vue_tasks/ .
RUN npm run build

# Этап сервера
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]