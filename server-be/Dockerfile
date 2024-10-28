FROM node:23.1-slim

WORKDIR /app

COPY server-be/package.json /app

RUN npm install

COPY ./server-be /app

CMD ["node", "index.mjs"]

EXPOSE 5050