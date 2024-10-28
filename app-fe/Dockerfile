FROM node:23.1-alpine

WORKDIR /app

COPY app-fe/package.json /app
COPY package-lock.json /app


RUN npm install

COPY ./app-fe /app

CMD ["npm", "start"]