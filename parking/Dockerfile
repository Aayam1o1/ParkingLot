FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org/ | python3 -
# RUN apt-get update && apt-get install -y gettext

# Add Poetry to PATH
# ENV PATH="/root/.local/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# COPY pyproject.toml poetry.lock* /app/
COPY requirements.txt /app/

# Install dependencies
# RUN poetry config virtualenvs.create false && pip install --no-dev
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]