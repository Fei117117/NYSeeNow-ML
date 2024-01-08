## NYSeeNow flask micro-service setup 

1. Create a folder for the NYC repository 

2. Navigate into the folder in the terminal and run _git intit_

3. Clone the repository using the command _git clone https://github.com/Fei117117/NYSeeNow-ML.git_

4. Open the NYSeeNow-ML on main branch in VSCode

5. Open the terminal in VScode and run:
   export FLASK_APP=predict.py
   flask run --port 5001
   
7. Now the flask app is running.
   
(some packages may need to be be installed:
pip install Flask
pip install numpy
pip install pandas
pip install haversine
pip install scikit-learn==1.2.0
pip install pycaret
pip install flask-cors)
