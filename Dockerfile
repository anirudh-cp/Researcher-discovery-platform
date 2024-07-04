# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY backend/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY backend /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the server
CMD ["python", "TornadoServer.py"]
