# Use the official Python base image
FROM python:3.11-slim

# Set the working directory to the root of the project
WORKDIR /app

# Install and update pip, then install Poetry for dependency management
RUN pip install --upgrade pip && \
    pip install poetry

# Configure Poetry: Disable virtualenv creation
RUN poetry config virtualenvs.create false

# Install system dependencies and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the Poetry configuration files into the image
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Create a group and user
RUN addgroup --system appgroup && adduser --system --group appuser

# Switch to non-root user
USER appuser

# Copy SQL and entrypoint script into the image
COPY --chown=appuser:appgroup sql/ /app/sql/
COPY --chown=appuser:appgroup scripts/ /app/scripts/
COPY --chown=appuser:appgroup entrypoint.sh /usr/local/bin/

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the application code into the image
COPY --chown=appuser:appgroup . /app

# Set the Python path
ENV PYTHONPATH=/app

# Set the entrypoint script to run when the container starts
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
