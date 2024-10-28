# FROM node:18-alpine

# WORKDIR /app

# COPY app-fe/package.json /app
# COPY app-fe/package-lock.json /app


# RUN npm install

# COPY ./app-fe /app

# CMD ["npm", "start"]


FROM nginx:stable-alpine

COPY /app/build/ /usr/share/nginx/html 