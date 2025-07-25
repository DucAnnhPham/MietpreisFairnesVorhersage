# MietpreisFairnesVorhersage
USW SS25 Team 8

Um dieses Projekt zu starten muss ertsmals eine venv erstellt werden
`python -m venv venv`
Diese muss aktiviert werden
Activate (`source venv/bin/activate` on WSL/Linux) the virutal environment.
On Windows with activate the environment with PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
or on Windows with Command Prompt:
```cmd
.\venv\Scripts\activate.bat
```
Die requirements müssen daraufhin installiert werden
`pip install -r requirements.txt`

Um dann die Daten zu speichern nutzt man dataScrapper.ipynb
Um diese Daten zu bereinigen nutzt man dataCleaner.ipynb
Um dann ein Modell zu trainieren, wobei das beste modell gespeichert wird nutzt man trainng.ipynb

Mit dem Modell kann man die Streamlit Application starten mit
Diese wird gestartet wenn man das venv aktiviert hat
```bash
streamlit run app.py
```
Die Anwendung wird dann normalerweise unter http://localhost:8501 verfügbar sein.


Die Datei plots.ipynb ist dazu da um sich einen überblick verschaffen zu können inwiefern welche Größen eine Auswirkung auf den Preis eines Angebots haben