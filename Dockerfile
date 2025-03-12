# filepath: /var/www/cloudfare/Dockerfile
# Usa una imagen base de Python
FROM python:3.11-slim

# Instala las dependencias necesarias y Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_126.0.6478.126-1_amd64.deb \
    && dpkg -i google-chrome-stable_126.0.6478.126-1_amd64.deb || apt-get -f install -y \
    && rm google-chrome-stable_126.0.6478.126-1_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia y configura el script de inicio
COPY docker_startup.sh /
RUN chmod +x /docker_startup.sh

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Configura el punto de entrada al script de inicio
ENTRYPOINT ["/docker_startup.sh"]