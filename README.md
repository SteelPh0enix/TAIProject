# TAIProject
Project for "Creating Internet Apps" subject on my uni

## Running the project

1. Make sure you have Python installed, at last 3.6 is recommended.
1. **(Optional)** I suggest creating virtualenv for the project. To do so, install package `virtualenv` using `pip` (`python -m pip install virtualenv`) and execute `python -m virtualenv venv`. Then, activate it by executing
    * `source venv/bin/activate` under Linux
    * `venv\scripts\activate.bat` under Windows
1. Install requirements from the project. From main repo directory, run `python -m pip install -r requirements.txt`
1. Enter `spectrogen` directory and run `python manage.py runserver` to start the application. It'll be available under `localhost:8000`
