cd src/scripts
echo "Setting up db..."
python setup_db.py
echo "Creating bundle..."
cd ../client
npm run prod
echo "Running server..."
cd ../
python run.py
