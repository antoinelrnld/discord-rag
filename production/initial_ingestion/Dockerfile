FROM node:22.12.0-slim

WORKDIR /usr/src/app

COPY ./production/initial_ingestion/src .
RUN npm install

CMD [ "npm", "start" ]