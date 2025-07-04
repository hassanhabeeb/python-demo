# Use a minimal Python 3.12 image
FROM python:3.12-slim

# Disable writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables needed for collectstatic to run successfully
# Make sure these are set in your docker-compose or .env file if using get_ssm_param

# Run collectstatic
#RUN python3 manage.py collectstatic --noinput || echo "collectstatic failed (probably missing SSM params)"

# Default command
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "collectstatic", "--noinput"] && ["python3", "manage.py", "runserver", "0.0.0.0:8000"]



