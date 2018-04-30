cd src/scripts
echo "Setting up db..."
python setup_db.py
echo "Creating bundle..."
cd ../client
npm run prod
echo "Running server..."
cd ../
gunicorn -w 4 -b 0.0.0.0:5000 run:app
