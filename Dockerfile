FROM node:lts-alpine3.20
WORKDIR /APP
WORKDIR /APP/SafeServer/'web-data-viz - SafeServer'
RUN cd /APP/SafeServer/'web-data-viz - SafeServer'; npm install
EXPOSE 3333
CMD [ "node", "app.js" ]
