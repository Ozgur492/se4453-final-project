# ============================================================
# Dockerfile — SE4453 Final Project (Group 9)
# Azure App Service Linux Container with SSH support
# ============================================================

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Copy SSH config and entrypoint script
COPY sshd_config /etc/ssh/
COPY init.sh .

# Install OpenSSH server, set root password, set permissions
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x ./init.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose web server port and SSH port
EXPOSE 8000 2222

# Start SSH + gunicorn via entrypoint script
ENTRYPOINT [ "./init.sh" ]
