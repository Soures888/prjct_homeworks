# Start from an Ubuntu image
FROM ubuntu:20.04

# Set noninteractive installation to avoid prompt during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libreadline-dev \
    libncurses5-dev \
    libpcre3-dev \
    libssl-dev \
    perl \
    make \
    wget \
    zlib1g-dev

# Define the versions of ngx_cache_purge and OpenResty
ARG OPENRESTY_VERSION=1.19.9.1
ARG NGX_CACHE_PURGE_VERSION=2.3.1

# Create a directory to store the sources
WORKDIR /tmp

# Download, extract, and compile ngx_cache_purge
RUN wget "https://github.com/torden/ngx_cache_purge/archive/refs/tags/v${NGX_CACHE_PURGE_VERSION}.tar.gz" && \
    tar -xvf v${NGX_CACHE_PURGE_VERSION}.tar.gz

# Download, extract, and compile OpenResty with ngx_cache_purge
RUN wget "https://openresty.org/download/openresty-${OPENRESTY_VERSION}.tar.gz" && \
    tar -xvf openresty-${OPENRESTY_VERSION}.tar.gz && \
    rm openresty-${OPENRESTY_VERSION}.tar.gz && \
    cd openresty-${OPENRESTY_VERSION} && \
    ./configure --with-pcre-jit --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_stub_status_module --with-http_auth_request_module --with-threads --with-luajit --add-module=../ngx_cache_purge-${NGX_CACHE_PURGE_VERSION} && \
    make -j$(nproc) && \
    make install

# Symlink OpenResty binaries into the PATH
RUN ln -sf /usr/local/openresty/bin/openresty /usr/local/bin/openresty && \
    ln -sf /usr/local/openresty/bin/resty /usr/local/bin/resty && \
    ln -sf /usr/local/openresty/nginx/sbin/nginx /usr/local/bin/nginx

# Expose ports
EXPOSE 80 443

# Define the entry point
ENTRYPOINT ["openresty", "-g", "daemon off;"]
