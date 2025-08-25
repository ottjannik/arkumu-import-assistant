# arkumu.nrw Import Assistant

arkumu.nrw Import Assistant ist eine Streamlit-Webanwendung, die Institutionen dabei unterstützt, ihre Metadaten vor dem Import auf arkumu.nrw auf Vollständigkeit, Konsistenz und Validität zu prüfen. Die App wurde im Rahmen der Praxisarbeit im Zertifikatskurs **Data Librarian 2024/2025** am ZBIW der TH Köln entwickelt.

---

## Inhaltsverzeichnis

- [Ziel der App](#ziel-der-app)
- [Projektstruktur](#projektstruktur)
- [Installation](#installation)
- [Starten der App](#starten-der-app)
- [Funktionsweise](#funktionsweise)
- [Beispieldaten für Tests](#beispieldatenn-für-tests)
- [Beispiel für JSON-Konfiguration](#beispiel-für-json-konfiguration)
- [Lizenz](#lizenz)

---

## Ziel der App

- Sicherstellung der **Datenqualität** vor dem Import in arkumu.nrw.
- Überprüfung von **Pflichtfeldern** (`Required`), **konditionalen Abhängigkeiten** (`Conditional`) und **alternativen Pflichtfeldern** (`Either/Or`).
- Erleichterung der **Fehleridentifikation**, sodass Probleme direkt in den Originaldatenquellen korrigiert werden können.

---

## Projektstruktur

Die Anwendung ist modular aufgebaut:

```
arkumu-import-assistant/
├─ .streamlit/            # Streamlit-Konfiguration (z. B. config.toml für Theme)
├─ configs/               # JSON-Profile und Validierungsregeln (z. B. KHM.json, HfMT.json)
├─ sample-data/           # Anonymisierte Beispieldaten für Tests (z. B. KHM)
│  └─ KHM/
├─ app.py                 # Hauptanwendung und Benutzeroberfläche
├─ licence.md             # Lizenzinformationen
├─ readme.md              # Projektbeschreibung, Installations- und Nutzungsanleitung
├─ requirements.txt       # Python-Abhängigkeiten
├─ stats.py               # Visualisierung von Statistiken
├─ utils.py               # Wiederverwendbare Funktionen zur Datenverarbeitung
├─ validation.py          # Validierungslogik für CSV-Dateien
└─ views.py               # Darstellung und Aufbereitung der Prüfergebnisse
```

---

## Installation

```bash
# Repository klonen
git clone https://github.com/ottjannik/arkumu-import-assistant
cd arkumu-import-assistant

# Virtuelle Umgebung (empfohlen)
python -m venv venv
source venv/bin/activate  # (oder venv\Scripts\activate auf Windows)

# Abhängigkeiten installieren
pip install -r requirements.txt
```

---

## Starten der App
```bash
streamlit run app.py
```

---

## Funktionsweise
1.	Profilwahl: Nutzer:innen wählen ein Profil, das die entsprechenden Validierungsregeln lädt.
2.	Dateiupload: Anschließend werden die für das Profil erforderlichen CSV-Dateien hochgeladen.
3.	Prüfung auf Vollständigkeit: Die App überprüft, ob alle erforderlichen Dateien vorhanden sind und ob Pflichtfelder ausgefüllt sind.
4.	Validierung von Abhängigkeiten: Konditionale Beziehungen zwischen Feldern werden geprüft.
5.	Ausgabe: Ergebnisse werden in zwei Modi dargestellt:
        - Kurzfassung: zeigt den Status jeder Datei.    
        - Detailansicht: tabellarische Übersicht fehlender oder inkorrekter Werte.

Hinweis: CSV-Dateien können innerhalb der App nicht bearbeitet werden. Änderungen müssen in der Originaldatenquelle erfolgen.

---

## Validierung
Die Validierung erfolgt über klar strukturierte Funktionen in validation.py. Die zentrale Funktion validate_dataframe prüft die CSV-Dateien auf Basis der definierten Regeln:
- Required: klassische Pflichtfelder, die in jeder Zeile ausgefüllt sein müssen (z. B. Projekt_ID, Originaltitel).
- Conditional: konditionale Abhängigkeiten, bei denen das Ausfüllen eines Feldes automatisch weitere Felder erforderlich macht (z. B. wenn ein Originaltitel vorhanden ist, muss auch die Originaltitel_Sprache angegeben werden).
- Either/Or: alternative Pflichtfelder, bei denen mindestens eines von mehreren Feldern befüllt sein muss (z. B. Angabe eines Anfangsdatums oder eines Enddatums).

Diese mehrstufige Regelstruktur erlaubt es, die heterogenen Anforderungen des arkumu.nrw-Datenmodells präzise abzubilden. Während einfache Pflichtfeldprüfungen nur die formale Vollständigkeit sicherstellen, tragen Conditional- und Either/Or-Regeln wesentlich dazu bei, die inhaltliche Konsistenz der Daten zu sichern und typische Fehlerquellen frühzeitig sichtbar zu machen.

---

## Beispieldaten für Tests

Um die Funktionalität der App auch ohne Zugriff auf die realen Metadaten zu testen, wurden Beispiel-CSV-Dateien bereitgestellt. Diese Dateien enthalten **anonymisierte Blinddaten** und spiegeln die Struktur des KHM-Profils wider.

Die Testdaten befinden sich im Verzeichnis:
```
sample-data/KHM/
```

Jede CSV-Datei entspricht einer der für das KHM-Profil erwarteten Tabellen und kann direkt über die App hochgeladen und validiert werden. So lässt sich der gesamte Workflow der App ausprobieren.

> Hinweis: Die Daten sind **synthetisch** und enthalten keinerlei reale personenbezogene Informationen.

---

## Beispiel für JSON-Konfiguration

Die JSON-Dateien befinden sich im Ordner configs/ und definieren die zu prüfenden Felder:
```json
{
  "validation_targets": {
    "projekte": {
      "filename": "00_Projekte.csv",
      "required": ["Projekt_ID", "Originaltitel"],
      "conditional": [
        {
          "if_filled": "Originaltitel",
          "then_required": ["Originaltitel_Sprache"]
        }
      ],
      "either_or": [
        {
          "columns": ["Eventanfangsdatum", "EventEnddatum"]
        }
      ]
    }
  }
}
```

--- 

## Lizenz
MIT License
