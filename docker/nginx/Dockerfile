FROM nginx:latest
MAINTAINER shen.charles@hotmail.com
ADD https://dl.eff.org/certbot-auto /usr/local/bin/certbot-auto
RUN chown root /usr/local/bin/certbot-auto && \
    chmod 0755 /usr/local/bin/certbot-auto && \
    certbot-auto -n --install-only