FROM serversideup/php:8.4-fpm-nginx-alpine

WORKDIR /var/www/html

#USER root
#RUN install-php-extensions gd redis

USER www-data

COPY --chown=www-data:www-data composer.* /var/www/html
RUN composer install --no-interaction --prefer-dist

COPY --chown=www-data:www-data . /var/www/html

RUN chown -R www-data:www-data /var/www/html
#    && chmod -R 755 /var/www/html/storage \
#    && chmod -R 755 /var/www/html/bootstrap/cache

EXPOSE 8080