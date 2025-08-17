# PDF_MERGE_WITH_TOC


## Motivation

Du möchtest mehrere einzelne PDF-Dokumente zu einem resultierenden PDF-Dokument
zusammenführen. Dabei sollen die einzelnen PDF-Dokumente nicht nur in einer
bestimmten Reihenfolge zusammengeführt werden, sondern es soll sich auf der 
ersten Seite des Dokuments ein Inhaltsverzeichnis befinden, über die jeweils
ersten Seiten der Dokumente verlinkt sind und ein Klick zur jeweiligen Seite
führt.


## Abhilfe

Folgende Schritte sind dabei durchzuführen:

1)	Die einzelnen PDF-Dokumente müssen Seitenweise in Bilddateien im Format `PNG`
	extrahiert werden. Die Dateinamen sollten dabei generisch und automatisch 
	nach einem Namensschema erstellt sein.
	
2)	Es ist durch den Benutzer zu definieren,

	1)	in welcher Reihenfolge die einzelnen PDF-Dokumente zusammenzuführen sind

	2)	welche der generierten Seiten im Inhaltsverzeichnis verlinkt sein 
		sollten und welchen Text der Link haben soll

	3)	welchen Namen das resultierende PDF-Dokument tragen soll

	4)	weitere Metadaten des resultierenden PDF-Dokuments, wie beispielsweise
	
		*	Titel
		*	Autor
		*	Thema
		*	Suchbegriffe
		*	Anwendung


## Schritte zur Initialisierung und Ausführung der Applikation mit dem Tool `UV`

### Voraussetzungen

Dieses Python Projekt benötigt zur Ausführug ein lokal installiertes Python 
in der Version 3.13 oder höher.

Als Python Paket- und Projekt-Manager kommt das Tool `uv` zum Einsatz.
Siehe hierzu auch [GitHub: `UV`](https://github.com/astral-sh/uv).

`uv` installieren mit Python und `pip`:

```
python -m pip install uv
```

### Source Code lokal installieren

Danach kann dieses Projekt von Github lokal als ZIP-Archiv heruntergeladen und 
entpackt oder alternativ per `git` geklont werden.

```
git clone https://github.com/marctrommen/pdf_merge_with_toc.git
cd pdf_merge_with_toc
```

Dies setzt voraus, dass `git` lokal installiert wurde. Siehe hierzu auch 
[Git installieren](https://git-scm.com/book/de/v2/Erste-Schritte-Git-installieren) 
oder [Git Download for Windows](https://git-scm.com/downloads/win)

### Virtuelles Environment erstellen

Lege eine `.venv`-Ordnerstruktur an (standardmäßig im Projektverzeichnis):

```
uv venv
```

###  Abhängigkeiten installieren aus `pyproject.toml`

`uv` erkennt die Abhängigkeiten automatisch im `pyproject.toml` unter 
`[project.dependencies]` und installiert sie ins `.venv` Verzeichnis.

```
uv pip install -r pyproject.toml
```

### (Optional) Lock-Datei generieren (für reproduzierbare Builds)

Erzeuge eine `uv.lock` Datei:

```
uv pip compile
```

Danach kann mit exakt gleichen Versionen gearbeiten werden über:

```
uv pip sync
```

### Virtuelle Umgebung aktivieren

Falls direkt mit python gearbeiten werden soll:

```
.venv\Scripts\activate.bat
```
(Windows)

```
source .venv/bin/activate
```
(Linux)

### Applikation starten

Nachdem dieses Python Projekt lokal verfügbar ist, kann die Applikation 
über zwei alternative Wege ausgeführt werden.

**Alternative 1: `uv`**

Im Projektverzeichnis kann folgender `uv` Befehl genutzt werden:

```
uv run src\main.py
```

**Alternative 2: `venv` und `Python`**

Im Projektverzeichnis kann das *virtual Environment* aktiviert werden (siehe oben).
Danach erfolgt die Ausführung im Projektverzeichnis über:

```
python src\main.py
```

**Alternative 3:** Bei Verwendung von Visual Studio Code als 
Entwicklungsumgebung ist noch der Ort des virtual Environment bekannt zu geben.

Um in Visual Studio Code (VS Code) ein bestehendes Python virtual Environment 
(venv) für die Ausführung der Datei main.py zu nutzen, ist folgendermaßen 
vorzugehen:

1.	VS Code öffnen und Projektordner laden

	Öffne VS Code und lade den Ordner, in dem sich `main.py` und das virtual 
	Environment befinden.

2.	Python-Interpreter auswählen

	1.	Öffne die Befehls-Palette mit:

		`Strg` + `Shift` + `P` (Windows/Linux)
	
	2.	Gib ein: `Python: Interpreter auswählen` 
		(Englisch: `Python: Select Interpreter`)
	
	3.	Wähle den Interpreter aus, der zu dem Virtual Environment gehört:
		
		```
		.venv/Scripts/python.exe
		```
		(bei Windows)

3.	Datei ausführen mit dem richtigen Interpreter

	Jetzt kann die Datei `main.py` mit dem virtuellen Environment ausgeführt
	werden, z. B. über:

	Rechtsklick auf die Datei und dann im Kontextmenü auswählen
	"Python-Datei im Terminal ausführen" (oder Englisch: "Run Python File in Terminal").

