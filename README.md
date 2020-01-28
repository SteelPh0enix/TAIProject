# TAIProject
Project for "Creating Internet Apps" subject on my uni

## Running the project

1. Make sure you have Python installed, at last 3.6 is recommended.
2. Also, make sure you have `ffmpeg` installed. On Windows, add directory with `ffmpeg.exe` to `%PATH%`.
3. **(Optional, but very recommended)** I suggest creating virtualenv for the project. To do so, install package `virtualenv` using `pip` (`python -m pip install virtualenv`) and execute `python -m virtualenv venv`. Then, activate it by executing
    * `source venv/bin/activate` under Linux
    * `venv\scripts\activate.bat` under Windows
4. Install requirements from the project. From main repo directory, run `python -m pip install -r requirements.txt`
5. Enter `spectrogen` directory. Create the database by running `python manage.py migrate`.
6. **(Optional, but very recommended)** Create superuser account, with name `admin` (because it's hard-coded in backend code, for now. Run `python manage.py createsuperuser`
7. Run `python manage.py runserver` to start the application. It'll be available under `localhost:8000`

## Maintenance

In case when adding spectrograms will always fail, due to video parsing error, update `youtube_dl` package.