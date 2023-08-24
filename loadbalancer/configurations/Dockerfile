# Use an official Alpine as a parent image
FROM alpine:latest

# Install dependencies required for building Nginx from source and the GeoIP module
RUN apk add --no-cache \
    gcc \
    wget \
    build-base \
    pcre \
    pcre-dev \
    zlib-dev \
    openssl-dev \
    geoip-dev \
    geoip \
    libmaxminddb-dev \

# Download and unpack Nginx source
RUN wget http://nginx.org/download/nginx-1.25.2.tar.gz && \
    tar -xzvf nginx-1.25.2.tar.gz

RUN wget https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/3.4.tar.gz && \
    tar -xzvf 3.4.tar.gz


# Compile and install Nginx with the ngx_http_geoip_module
WORKDIR nginx-1.25.2

RUN ./configure --with-compat --add-dynamic-module=../ngx_http_geoip2_module-3.4 && \
    make && \
    make install

# Create a symbolic link for convenience
RUN ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx

# Cleanup: Remove unnecessary packages and files to reduce the image size
RUN apk del gcc build-base wget pcre-dev zlib-dev openssl-dev && \
    rm -rf nginx-1.21.1* && \
    rm -rf /var/cache/apk/*

# Expose ports 80 and 443
EXPOSE 80 443

# Start Nginx in the foreground (so Docker container doesn't exit)
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;", "-c", "/usr/local/nginx/conf/nginx.conf"]
