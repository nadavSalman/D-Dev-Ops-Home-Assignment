# FROM node:18-alpine

# WORKDIR /app

# COPY app-fe/package.json /app
# COPY app-fe/package-lock.json /app


# RUN npm install

# COPY ./app-fe /app

# CMD ["npm", "start"]


# FROM nginx:stable-alpine

# COPY ./app-fe/build /usr/share/nginx/html 




# Stage 1: Build the React app
FROM node:lts as builder
WORKDIR /app
COPY ./app-fe/package*.json ./
RUN npm install
COPY ./app-fe .
RUN npm run build
# Stage 2: Create the production image
FROM nginx:latest
COPY --from=builder ./app-fe/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]