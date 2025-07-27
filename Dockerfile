# Use official Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Run entrypoint (migrations + start server)
ENTRYPOINT ["./docker-entrypoint.sh"]
