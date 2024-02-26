FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY /etc/nginx/ssl/fullchain.pem /etc/nginx/ssl/fullchain.pem
COPY /etc/nginx/ssl/privkey.pem /etc/nginx/ssl/privkey.pem