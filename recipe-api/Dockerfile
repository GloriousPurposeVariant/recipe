# Use Python 3.8.10 as the base image
FROM python:3.8.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Copy entrypoint scripts
COPY entrypoint.sh /app/

# Create a non-root user
RUN useradd -ms /bin/bash myuser

# Set permissions and ownership
RUN chmod +x /app/entrypoint.sh
RUN chown -R myuser:myuser /app

# Switch to the new user
USER myuser

# Set default entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]