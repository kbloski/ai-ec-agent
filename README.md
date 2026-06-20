Python versja 3.14

Tworzenie venv 
python.exe -m venv venv
D:\Python\3.14\python.exe -m venv venv

// Instalacja pakietow
python.exe -m pip install -r requirements.txt
D:\Python\3.14\python.exe -m pip install -r requirements.txt

// Zapisywanie nowej konfiguracji pakietow 
pip freeze > requirements.txt (musi byc wywolane w venv)

Aby skorzysta z venv w powershell
.\venv\Scripts\Activate.ps1     

Aby uruchomi aplikacje
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001



