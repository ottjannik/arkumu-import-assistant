# arkumu.nrw Import Assistant  
*Theoretische Ausarbeitung zur Praxisarbeit im Rahmen des Zertifikatskurses Data Librarian am ZBIW der TH Köln (2025/2025)*

GitHub Repositorium: [https://github.com/ottjannik/arkumu-import-assistant](https://github.com/ottjannik/arkumu-import-assistant)

---

# Inhaltsverzeichnis

- [Zusammenfassung](#zusammenfassung)
1. [Einleitung und Kontext](#1-einleitung-und-kontext)
2. [Hintergrund und theoretische Grundlagen](#2-hintergrund-und-theoretische-grundlagen)
3. [Projektbeschreibung und Umsetzung](#3-projektbeschreibung-und-umsetzung)
4. [Ergebnisse](#4-ergebnisse)
5. [Diskussion und kritische Reflexion](#5-diskussion-und-kritische-reflexion)
6. [Fazit](#6-fazit)
- [Literaturverzeichnis](#literaturverzeichnis)
- [Anhang](#anhang)
  - [A.1 JSON-Beispielkonfiguration](#a1-json-beispielkonfiguration)
  - [A.2 Code-Auszug `validation.py`](#a2-code-auszug-validationpy)
  - [A.3 Screenshots der Anwendung](#a3-screenshots-der-anwendung)

---

## Zusammenfassung

Die Arbeit stellt den **arkumu.nrw Import Assistant** vor, eine in Python entwickelte Anwendung zur Unterstützung der Datenprüfung im Rahmen des Projekts arkumu.nrw. Die App ermöglicht es, aus Hochschularchiven exportierte CSV-Dateien auf **Vollständigkeit** zu überprüfen und stellt die Ergebnisse in einer benutzerfreundlichen Oberfläche dar. Damit bietet die Anwendung eine erste, praxisnahe Unterstützung bei der Vorprüfung von Metadatenqualität, die perspektivisch zu einem vollwertigen Validierungswerkzeug ausgebaut werden kann.

---

## 1. Einleitung und Kontext

Die Erschließung, Verfügbarhaltung und dauerhafte Archivierung multimedialer künstlerischer Bestände stellt Bibliotheken, Archive und Museen vor besondere Herausforderungen. Mit dem Projekt arkumu.nrw wird ein landesweites Portal geschaffen, das die qualitativ hochwertige Erschließung, Standardisierung und Archivierung der Bestände der Kunst- und Musikhochschulen Nordrhein-Westfalens bündelt. Ziel ist es, die digitalen Objekte und Metadaten der beteiligten Hochschulen in die Langzeitarchivierungsstrukturen des Landes NRW zu überführen und zugleich ihre wissenschaftliche, künstlerische und öffentliche Nutzung durch einheitliche Metadatenstandards und eine benutzerfreundliche Oberfläche zu fördern.

Die fünf beteiligten Kunst- und Musikhochschulen verfügen über sehr unterschiedliche Ausgangsbedingungen: Während einige bislang keine systematischen Archivierungsstrukturen aufgebaut haben, verwalten andere seit Jahrzehnten gewachsene Bestände in etablierten Datenbanksystemen. Um die heterogenen Ausgangslagen der beteiligten Hochschulen in eine gemeinsame Infrastruktur zu überführen, ist ein einheitliches Datenmodell notwendig, das verbindliche Pflichtfelder und konsistente Strukturen vorgibt.  

Die App setzt an dem Punkt an, an dem die Daten aus den Hochschularchiven exportiert werden: Sie ermöglicht Projektbeteiligten, diese CSV-Dateien vorab auf ihre Übereinstimmung mit den **Pflichtfeld-Vorgaben** des arkumu.nrw-Datenmodells zu prüfen. Damit unterstützt sie eine erste Form der Qualitätssicherung, bevor die Daten in die zentrale Infrastruktur übernommen werden.

Nach dieser vorbereitenden Prüfung werden die Metadaten von den Projektbeteiligten in eine vom **IT Center University of Cologne (ITCC)** entwickelte Django-Anwendung überführt und anschließend von dort an das Hochschulbibliothekszentrum sowie dessen Langzeitverfügbarkeitsstrukturen übergeben.  

Die App selbst ist somit nicht Teil des Importprozesses, sondern erfüllt die Funktion einer vorgeschalteten **Vorprüfung auf Vollständigkeit**.

---

## 2. Hintergrund und theoretische Grundlagen

Die Sicherung und Archivierung multimedialer Forschungs- und Kunstbestände erfordert eine hohe Datenqualität. Fehlende Pflichtangaben, uneinheitliche Schreibweisen oder inkonsistente Verknüpfungen führen schnell zu Inkompatibilitäten, die den Importprozess behindern oder Nacharbeiten erfordern.

Im Datenqualitätsmanagement werden drei Dimensionen unterschieden:  
- **Vollständigkeit**: alle notwendigen Felder und Dateien sind vorhanden.  
- **Konsistenz**: die Daten sind widerspruchsfrei und Abhängigkeiten werden korrekt eingehalten.  
- **Validität**: die Inhalte entsprechen den geforderten Standards und semantischen Regeln.  

Während klassische Validierungsframeworks (z. B. XML-Schema, JSON-Schema, OpenRefine) generische Prüfungen ermöglichen, braucht arkumu.nrw ein maßgeschneidertes Werkzeug, da die Metadaten spezifische Anforderungen der Kunst- und Musikhochschulen erfüllen müssen.  

Die theoretische Grundlage der App orientiert sich an den FAIR-Prinzipien (Findable, Accessible, Interoperable, Reusable). Indem die App die Vollständigkeit prüft und mittelfristig um Konsistenz- und Validitätsprüfungen erweitert werden soll, trägt sie zur **Auffindbarkeit** und **Interoperabilität** bei und unterstützt langfristig die **Nachnutzbarkeit** der Bestände.

---

## 3. Projektbeschreibung und Umsetzung

Im Rahmen der Arbeit wurde mit dem **arkumu.nrw Import Assistant** eine leichtgewichtige Web-Anwendung entwickelt, die den Validierungsprozess unterstützt. Sie ermöglicht Projektbeteiligten, exportierte CSV-Dateien auf **Vollständigkeit** zu prüfen.  

Die App wurde in Python programmiert und nutzt das Framework **Streamlit**. Die Nutzer:innen wählen ein Validierungsprofil (JSON-basiert), laden die zugehörigen CSV-Dateien hoch, und die App prüft anschließend:  
- ob alle erforderlichen Dateien vorhanden sind,  
- ob die definierten Pflichtfelder ausgefüllt wurden.  

Die Ergebnisse werden in einer Übersicht und tabellarisch dargestellt. Eine direkte Bearbeitung der CSV-Dateien ist bewusst nicht möglich, um die Integrität der Quelldaten zu gewährleisten.  

Die aktuelle Version der App ist in zwei **Tabs** aufgeteilt:  
- **Übersicht**: Zeigt eine Zusammenfassung der hochgeladenen Metadaten in Form von Kennzahlen (z. B. Anzahl Projekte, Akteur:innen, Objekte) sowie eine Visualisierung der Dateiendungen.  
- **Pflichtfeldprüfung**: Prüft die Vollständigkeit der Pflichtfelder und zeigt den Status jeder Datei in einer Ampel-Logik an.

Die Software ist modular aufgebaut (`app.py`, `utils.py`, `validation.py`, `views.py`, `stats.py`). Validierungsregeln sind in JSON-Profilen abgelegt.  

Aktuell sind folgende Regeltypen implementiert:  
- **Required Rules** (Pflichtfelder)  
- **Conditional Rules** (Bedingungen, z. B. Sprache muss angegeben sein, wenn ein Titel vorhanden ist)  
- **Either/Or Rules** (mindestens eines von mehreren Feldern muss ausgefüllt sein)  

Konsistenz- und Validitätsprüfungen (z. B. Dublettenprüfung, Prüfung von Datentypen, semantische Abhängigkeiten) sind für künftige Versionen vorgesehen.

---

## 4. Ergebnisse

Die aktuelle Version des **arkumu.nrw Import Assistant** leistet:  
- **Vollständigkeit:** Prüfung, ob alle Dateien und Pflichtfelder vorhanden sind.  

Damit wird ein erster, wichtiger Schritt in der Qualitätssicherung abgedeckt. Konsistenz und Validität sind noch nicht Bestandteil der Implementierung, aber in der Architektur mitgedacht.  

Nutzer:innen erhalten eine visuelle Übersicht zum Status der Dateien und eine Detailansicht mit Hinweisen zu fehlenden Pflichtfeldern.

---

## 5. Diskussion und kritische Reflexion

**Erfolge:**  
- Schnelle Umsetzung dank Streamlit.  
- Intuitive Bedienbarkeit.  
- Modularer Aufbau und JSON-Konfigurationen für flexible Anpassbarkeit.  
- Erste Implementierung einer automatisierten Pflichtfeldprüfung.  

**Einschränkungen:**  
- Nur CSV-Dateien werden unterstützt.  
- Keine Konsistenz- oder Validitätsprüfungen.  
- Keine automatische Fehlerkorrektur.  
- Abhängigkeit von korrekt gepflegten JSON-Profilen.  

**Nächste Schritte:**  
- Erweiterung auf **Konsistenz- und Validitätsprüfungen** (z. B. Dubletten, kontrollierte Vokabulare, Datentypen).  
- Unterstützung weiterer Datenquellen/Dateiformate.  
- Anbindung an institutionelle Datenrepositorien.  
- Mehrsprachigkeit (DE/EN).  
- Detailliertere Berichte und Korrekturvorschläge.  

---

## 6. Fazit

Der **arkumu.nrw Import Assistant** ist ein praxisnahes Werkzeug, das aktuell eine **Vorprüfung auf Vollständigkeit** ermöglicht. Damit trägt er zur Verbesserung der Datenqualität vor dem Import in arkumu.nrw bei.  

Die langfristige Zielsetzung bleibt der Ausbau zu einem umfassenden Validierungswerkzeug, das auch **Konsistenz** und **Validität** prüft. Erst in dieser Form erfüllt die App die vollständigen Anforderungen eines systematischen Datenqualitätsmanagements.  

Die Anwendung zeigt aber schon jetzt, wie datenqualitative Anforderungen in einer benutzerfreundlichen Umgebung operationalisiert werden können und welche Rolle Tools dieser Art im Kontext von **FAIR Data** und **Data Librarianship** einnehmen können.

---

## Anhang  

### A.1 JSON-Beispielkonfiguration  
```json
"validation_targets": {
    "projekte": {
      "filename": "00_Projekte.csv",
      "required": [
        "Projekt_ID"
      ],
      "conditional": [
        {
          "if_filled": "Originaltitel",
          "then_required": ["Originaltitel_Sprache"]
        }
      ],
      "either_or": []
    }
}
```

### A.2 Code-Auszug validation.py
```python
# -------------------
# Conditional prüfen
# -------------------
conditional_rules = rules.get("conditional", [])
conditional_errors = []

for rule in conditional_rules:
    if_col = rule.get("if_filled")
    then_cols = rule.get("then_required", [])
    if if_col in df.columns:
        for then_col in then_cols:
            if then_col not in df.columns:
                conditional_errors.append(pd.DataFrame({
                    "Fehlende_Spalte": [then_col],
                    "Fehlerbeschreibung": ["Spalte fehlt"]
                }))
                continue
            missing_rows = df[
                df[if_col].notna() & (df[if_col].astype(str).str.strip() != "") &
                (df[then_col].isna() | (df[then_col].astype(str).str.strip() == ""))
            ]
            if not missing_rows.empty:
                conditional_errors.append(extract_error_rows(
                    missing_rows, [if_col, then_col],
                    f"{if_col} ausgefüllt, aber {then_col} leer"
                ))
```