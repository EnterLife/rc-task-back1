:: Activate environment venv
call .\venv\Scripts\activate

:: Start worker.py
py main.py

TIMEOUT /T 10 /NOBREAK
exit