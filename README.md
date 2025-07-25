# MietpreisFairnesVorhersage
**USW SS25 – Team 8**
**Teammitglieder:**
- **Duc Anh Pham** (589879)
- **Manh Hai Nguyen** (588555)

Dieses Projekt dient der Analyse und Vorhersage der Fairness von Mietpreisen anhand gesammelter Wohnungsanzeigen.

---

## SETUP
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

Die requirements müssen daraufhin installiert werden, um die benötigten Pakete zu installieren:
`pip install -r requirements.txt`


## Projektstruktur
```
HTML Anzeigen aus Berlin werden in einem Ordner namens ALL DATA IMMOWELT gespeichert
cvs Dateien mit den Daten aus den Anzeigen werden in einem Ordner namens data gespeichert
Der models Ordner enthält die gespeicherten Modelle, die durch das Training der Notebooks erstellt wurden (diese Dateien werden von der Streamlit App genutzt)
Die ausführbaren Notebooks sind in einem Ordner namens notebooks gespeichert
```

## Nutzung der Notebooks
```
-> Notebooks/Dateien sollten in dieser Reihenfolge ausgeführt werden:
dataScrapper.ipynb: Jupyter Notebook zum Scrappen der Wohnungsdaten

dataCleaner.ipynb: Jupyter Notebook zum Bereinigen und Vorbereiten der Daten

trainng.ipynb: Jupyter Notebook zum Trainieren des Modells, wobei das beste Modell gespeichert wird

app.py: Streamlit Anwendung zur Fairness-Vorhersage von Mietpreisen
```
Zusatz-Notebook zur Visualisierung der gescrapten Daten um Zusammenhang zwischen Daten zu erkennen
```
plots.ipynb: Jupyter Notebook zum Visualisieren der Daten
```

## Ausführen der Anwendung
Mit dem Modell, das durch die Ausfürhung der Notebooks gespeichert wurde, kann man die Streamlit Application starten.
Diese wird gestartet, wenn man das venv aktiviert hat und man folgen Command in der Kommandozeile ausführt:
`streamlit run app.py`
Die Anwendung wird dann normalerweise unter http://localhost:8501 verfügbar sein.