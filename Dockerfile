FROM node:lts-alpine3.20
WORKDIR /
COPY ./web-data-viz-safeserver .
RUN npm i
EXPOSE 3333
CMD [ "node", "app.js" ]
