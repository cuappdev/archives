#!/bin/bash

# Step 0:
# Delete the databases if they exist
echo \
  "DROP DATABASE IF EXISTS pcasts_ml_db_dev;" \
  "DROP DATABASE IF EXISTS test_pcasts_ml_db_dev;" \
    | mysql --user=$DB_USERNAME --password=$DB_PASSWORD

# Step 1:
# Create the databases
echo \
  "CREATE DATABASE pcasts_ml_db_dev;" \
  "CREATE DATABASE test_pcasts_ml_db_dev;" \
    | mysql --user=$DB_USERNAME --password=$DB_PASSWORD

# Step 2:
# Migrate everything
cd src/scripts
python setup_db.py dev
python setup_db.py test
cd ../..

# Step 3:
# Load the test data
python src/scripts/load_data.py dev
python src/scripts/load_data.py test
