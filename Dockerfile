# filepath: /var/www/cloudfare/Dockerfile
# Usa una imagen base de Python
# Use an image with a desktop environment
FROM kasmweb/desktop:1.16.0-rolling-daily

# Set environment variables to avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Instala las dependencias necesarias y Google Chrome
USER root
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        wget \
        gnupg \
        ca-certificates \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libxss1 \
        libxtst6 \
        libnss3 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        x11-apps \
        fonts-liberation \
        libappindicator3-1 \
        libu2f-udev \
        libvulkan1 \
        libdrm2 \
        xdg-utils \
        xvfb \
        libasound2 \
        libcurl4 \
        libgbm1 \
        && rm -rf /var/lib/apt/lists/*

# Download and install specific version of Google Chrome
RUN wget https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_126.0.6478.126-1_amd64.deb && \
    dpkg -i google-chrome-stable_126.0.6478.126-1_amd64.deb && \
    rm google-chrome-stable_126.0.6478.126-1_amd64.deb

# Install Python dependencies including pyvirtualdisplay
RUN pip3 install --upgrade pip
RUN pip3 install pyvirtualdisplay

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --ignore-installed -r requirements.txt

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Copia y configura el script de inicio
COPY docker_startup.sh /
RUN chmod +x /docker_startup.sh

# Configura el punto de entrada al script de inicio
ENTRYPOINT ["/docker_startup.sh"]