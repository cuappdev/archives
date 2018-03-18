cd src/scripts
echo "Setting up db..."
python setup_db.py
echo "Running server..."
cd ..
python run.py
