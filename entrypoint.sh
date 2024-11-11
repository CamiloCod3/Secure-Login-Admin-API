#!/bin/bash

echo "Starting entrypoint script..."

# Wait for the database to be ready
echo "Waiting for database to be ready..."
RETRIES=10
while ! pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" > /dev/null 2>&1; do
  echo "Waiting for database... $((RETRIES--))"
  sleep 1
  if [ $RETRIES -lt 0 ]; then
    echo "Error: Database not ready after maximum retries."
    exit 1
  fi
done
 
echo "Initializing database for user management..."
# Execute the SQL script, assuming init_users.sql is idempotent and can safely be run multiple times
PGPASSWORD=$POSTGRES_PASSWORD psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -a -f /app/sql/init_users.sql

echo "Ensuring admin user is created..."
# Create the admin user
python /app/scripts/create_admin.py

echo "Starting application..."
exec "$@"