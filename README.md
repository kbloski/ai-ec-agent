Python versja 3.14

Tworzenie venv 
python.exe -m venv venv
D:\Python\3.14\python.exe -m venv venv

// Instalacja pakietow
.\venv\Scripts\python.exe -m pip install -r requirements.txt
(w venv)

// Zapisywanie nowej konfiguracji pakietow 
.\venv\Scripts\python.exe pip freeze > requirements.txt (musi byc wywolane w venv)

Aby skorzysta z venv w powershell
.\venv\Scripts\Activate.ps1     

Aby uruchomi aplikacje
.\venv\Scripts\python.exe .\main.py      

