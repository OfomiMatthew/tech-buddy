#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p instance
mkdir -p app/static/uploads/messages/files
mkdir -p app/static/uploads/messages/images
mkdir -p app/static/uploads/messages/voice

# Run migrations
python migrate_db.py
python migrate_ai_tables.py

echo "Build completed successfully!"
