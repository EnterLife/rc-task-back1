:: Create environment with name venv
call python -m venv venv

:: Activate environment venv
call .\venv\Scripts\activate

:: Upgrade pip
call python -m pip install --upgrade pip

:: Install libraries from requirements.txt
call pip install -r requirements.txt

pause