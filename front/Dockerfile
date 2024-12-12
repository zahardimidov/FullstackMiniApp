FROM node:alpine as build

COPY package.json package.json
RUN npm install

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL $REACT_APP_API_URL

COPY . .
RUN npm run build


FROM nginx:stable-alpine

COPY --from=build /build /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD [ "nginx", "-g", "daemon off;" ]