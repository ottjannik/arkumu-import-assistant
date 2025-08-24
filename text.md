# arkumu.nrw Import Assistant  
*Theoretische Ausarbeitung zur Praxisarbeit*

[Repositorium](https://github.com/ottjannik/arkumu-import-assistant)

---

# Inhaltsverzeichnis

- Abstract
- 1. Einleitung und Kontext
- 2. Hintergrund und theoretische Grundlagen
- 3. Projektbeschreibung und Umsetzung
- 4. Ergebnisse
- 5. Diskussion und kritische Reflexion
- 6. Fazit
- Literaturverzeichnis
- Anhang
  - A.1 JSON-Beispielkonfiguration
  - A.2 Code-Auszug `validation.py`
  - A.3 Screenshots der Anwendung

---

## Abstract

Die Arbeit stellt den **arkumu.nrw Import Assistant** vor, eine in Python entwickelte Anwendung zur Validierung von Metadaten im Rahmen des Projekts arkumu.nrw. Die App überprüft aus Hochschularchiven exportierte CSV-Dateien auf Vollständigkeit, Konsistenz und Validität und stellt sie in einer benutzerfreundlichen Oberfläche dar. Damit ermöglicht sie eine effiziente Vorprüfung der Datenqualität und unterstützt die Anschlussfähigkeit an das arkumu.nrw-Datenmodell.

---

## 1. Einleitung und Kontext

Die Erschließung, Verfügbarhaltung und dauerhafte Archivierung multimedialer künstlerischer Bestände stellt Bibliotheken, Archive und Museen vor besondere Herausforderungen. Mit dem Projekt arkumu.nrw wird ein landesweites Portal geschaffen, das die qualitativ hochwertige Erschließung, Standardisierung und Archivierung der Bestände der Kunst- und Musikhochschulen Nordrhein-Westfalens bündelt. Ziel ist es, die digitalen Objekte und Metadaten der beteiligten Hochschulen in die Langzeitarchivierungsstrukturen des Landes NRW zu überführen und zugleich ihre wissenschaftliche, künstlerische und öffentliche Nutzung durch einheitliche Metadatenstandards und eine benutzerfreundliche Oberfläche zu fördern.

Die fünf beteiligten Kunst- und Musikhochschulen verfügen über sehr unterschiedliche Ausgangsbedingungen: Während einige bislang keine systematischen Archivierungsstrukturen aufgebaut haben und Daten auf lokalen Speichermedien ablegen, verwalten andere seit Jahrzehnten gewachsene Bestände in etablierten Datenbanksystemen. Um diese heterogenen Ausgangslagen in eine gemeinsame Infrastruktur überführen zu können, ist ein einheitliches Datenmodell erforderlich, das verbindliche Pflichtfelder und konsistente Strukturen vorgibt.

Hier setzt die entwickelte App an: Sie unterstützt Projektbeteiligte dabei, die aus den Hochschularchiven exportierten Metadaten in Form von CSV-Dateien vorab zu prüfen und deren Konformität mit den im arkumu.nrw-Datenmodell definierten Pflichtfeldern zu validieren. Auf diese Weise lässt sich bereits vor dem eigentlichen Import sicherstellen, dass die Daten konsistent und anschlussfähig sind und ohne grundlegende Korrekturen in den Workflow eingebracht werden können.

Nach dieser vorbereitenden Validierung werden die Metadaten von den Projektbeteiligten in eine vom **IT Center University of Cologne (ITCC)** entwickelte Django-Anwendung überführt und anschließend von dort aus an das Hochschulbibliothekszentrum (`hbz`) sowie dessen Langzeitverfügbarkeitsstrukturen übergeben. Die App selbst ist damit nicht Teil des Importprozesses, sondern erfüllt die Funktion einer vorgeschalteten Qualitätssicherung: Sie bietet eine strukturierte Ansicht der Metadaten, überprüft die Erfüllung von Pflichtfeldern und stellt so sicher, dass die Daten zuverlässig für die weitere Verarbeitung vorbereitet sind.

---

## 2. Hintergrund und theoretische Grundlagen

Die Verarbeitung und Archivierung multimedialer Forschungs- und Kunstbestände erfordert eine hohe Datenqualität, um deren langfristige Verfügbarkeit und Nachnutzbarkeit zu gewährleisten. Insbesondere bei Metadaten treten dabei mehrere Herausforderungen auf: Zum einen sind die Ausgangsdaten oft heterogen, da sie aus unterschiedlichen Systemen exportiert werden und unterschiedliche Strukturen, Formate und Terminologien aufweisen. Zum anderen müssen die Metadaten vollständig und valide sein, um in standardisierte Infrastrukturen wie die Langzeitarchivierungsumgebung des Hochschulbibliothekszentrums (hbz) integriert werden zu können. Fehlende Pflichtangaben, uneinheitliche Schreibweisen oder inkonsistente Verknüpfungen führen schnell zu Inkompatibilitäten, die den Importprozess behindern oder Nacharbeiten erforderlich machen.

Zur Sicherstellung von Konsistenz und Anschlussfähigkeit wurden in arkumu.nrw verbindliche Pflichtfelder sowie ein gemeinsames Datenmodell definiert (Link einfügen). Die Überprüfung der Einhaltung dieser Vorgaben ist ein klassischer Anwendungsfall der Datenvalidierung, die als Teil des übergeordneten Datenqualitätsmanagements verstanden werden kann. Validierung umfasst dabei nicht nur die formale Prüfung, ob bestimmte Felder ausgefüllt sind, sondern auch die semantische Kontrolle von Abhängigkeiten und Konditionalitäten (z. B. „Wenn ein Projekt einen Projekttitel hat, muss für diesen auch eine Sprachauszeichnung gemäß entsprechendem ISO-Standard vorliegen.“).

Für die technische Umsetzung existieren im Bereich der Datenvalidierung bereits verschiedene Ansätze und Tools, etwa Schema-Validierungen für XML oder JSON, Prüfroutinen in Datenbankmanagementsystemen oder Validierungsframeworks wie OpenRefine für tabellarische Daten. Im Kontext von arkumu.nrw reicht jedoch kein generisches Werkzeug aus, da die zu verarbeitenden Metadaten spezifischen fachlichen und strukturellen Anforderungen unterliegen, die durch ein maßgeschneidertes Validierungssystem abgedeckt werden müssen.

Die theoretische Grundlage der App orientiert sich zugleich an den **FAIR-Prinzipien** (Findable, Accessible, Interoperable, Reusable), die inzwischen als Leitlinie für den Umgang mit Forschungsdaten etabliert sind. Indem die App sicherstellt, dass Metadaten konsistent und standardkonform vorliegen, trägt sie unmittelbar zur Auffindbarkeit (Findability) und Interoperabilität bei. Langfristig wird so die Nachnutzbarkeit (Reusability) wissenschaftlich und künstlerisch relevanter Bestände unterstützt.

---

## 3. Projektbeschreibung und Umsetzung

Im Rahmen der Arbeit wurde mit dem **arkumu.nrw Import Assistant** eine leichtgewichtige Web-Anwendung entwickelt, die den Validierungsprozess der Metadaten unterstützt und Projektbeteiligten eine einfache Möglichkeit zur Überprüfung ihrer CSV-Exporte bietet. Die App wurde in Python programmiert und nutzt das Framework **Streamlit**, das eine schnelle Entwicklung interaktiver Weboberflächen mit geringem technischem Aufwand ermöglicht.

Die Software folgt einer modularen Struktur:
- Die zentrale Steuerung erfolgt über die Datei `app.py`, in der die Benutzeroberfläche und die Ablaufsteuerung definiert sind.
- Wiederverwendbare Funktionen zur Datenverarbeitung befinden sich in `utils.py`.
- Die Validierungslogik, also die Überprüfung der Pflichtfelder und konditionalen Abhängigkeiten, ist in `validation.py` gekapselt.
- Die visuelle Darstellung und Aufbereitung der Ausgaben wird in `views.py` organisiert.

Darüber hinaus ermöglichen Konfigurationsdateien im JSON-Format die Definition projektspezifischer Profile (z. B. für die KHM) sowie die Ablage der Validierungsregeln. Ein Beispiel für eine minimale JSON-Konfiguration ist in **Anhang A.1** dargestellt. Die vollständigen Profile können über das Repositorium eingesehen werden.

Die Validierung selbst erfolgt über klar strukturierte Funktionen, die in `validation.py` implementiert sind. Eine Kernfunktion, die die Überprüfung von **Conditional Rules** übernimmt, ist exemplarisch in **Anhang A.2** aufgeführt. Dieser Codeausschnitt zeigt, wie Abhängigkeiten zwischen Feldern überprüft werden: Ist ein bestimmtes Feld ausgefüllt (z. B. *Originaltitel*), so wird automatisch gefordert, dass abhängige Felder ebenfalls befüllt sind (z. B. *Originaltitel_Sprache*). Auf diese Weise können semantische Beziehungen abgebildet und Fehlerquellen bei der Datenübertragung frühzeitig erkannt werden.


- **Required:** klassische Pflichtfelder, die in jeder Zeile gefüllt sein müssen (z. B. `Projekt_ID`, `Originaltitel`).  
- **Conditional:** konditionale Abhängigkeiten, bei denen das Ausfüllen eines Feldes automatisch weitere Felder erforderlich macht (z. B. wenn ein *Originaltitel* vorhanden ist, muss auch die *Originaltitel_Sprache* angegeben werden).  
- **Either/Or:** alternative Pflichtfelder, bei denen mindestens eines von mehreren Feldern befüllt sein muss (z. B. Angabe eines *Anfangsdatums* oder eines *Enddatums*).

Diese mehrstufige Unterscheidung erlaubt es, die heterogenen Anforderungen des arkumu.nrw-Datenmodells präzise abzubilden. Während einfache Pflichtfeldprüfungen nur die formale Vollständigkeit sicherstellen, tragen die **Conditional**- und **Either/Or**-Regeln wesentlich dazu bei, die inhaltliche Konsistenz der Daten zu sichern und typische Fehlerquellen bei der Datenübertragung frühzeitig sichtbar zu machen.

Die Funktionalität der Anwendung umfasst mehrere aufeinanderfolgende Schritte:
1. **Profilwahl:** Nutzer:innen wählen ein Profil, das die jeweils geltenden Validierungsregeln lädt.  
2. **Dateiupload:** Anschließend werden die für das Profil erforderlichen CSV-Dateien hochgeladen.  
3. **Prüfung auf Vollständigkeit:** Die App kontrolliert, ob alle benötigten Dateien vorhanden sind und ob die darin enthaltenen Pflichtfelder ausgefüllt wurden.  
4. **Validierung von Abhängigkeiten:** Konditionale Beziehungen zwischen Feldern werden überprüft (z. B. bestimmte Rollen bei bestimmten Ereignistypen).  
5. **Ausgabe:** Das Ergebnis der Prüfung wird in zwei Modi bereitgestellt:
   - **Kurzfassung:** klare Erfolgsmeldung oder Fehlerhinweis je Datei.  
   - **Detailansicht:** tabellarische Übersicht, die fehlende oder ungültige Werte präzise aufzeigt.

**Wichtig:** CSV-Dateien können innerhalb der App nicht bearbeitet werden. Änderungen müssen in der Ursprungsdatenbank vorgenommen werden, da dort die Originaldaten gespeichert sind. Eine Bearbeitung direkt in den CSV-Dateien würde das Problem nur lokal ändern und beim nächsten Export würden die Fehler erneut auftreten. Die App dient daher ausschließlich der Anzeige, an welchen Stellen Pflichtfelder fehlen oder inkorrekt ausgefüllt sind, um eine gezielte Korrektur in der Originaldatenquelle zu ermöglichen.

---

## 4. Ergebnisse
Mit der Entwicklung des **arkumu.nrw Import Assistant** konnten die im Vorfeld definierten Hauptziele erreicht werden:
- **Vollständigkeit:** alle erforderlichen Dateien liegen vor.
- **Konsistenz:** Pflichtfelder und Abhängigkeiten sind korrekt ausgefüllt.
- **Validität:** transparente, nachvollziehbare Auswertung der Datenqualität.

Die Funktionalität konnte erfolgreich anhand von Testdaten demonstriert werden. Nutzer:innen erhalten sowohl eine kompakte Rückmeldung zum Status der einzelnen Dateien als auch die Möglichkeit, gezielt einzelne Problemstellen nachzuvollziehen.

Durch den modularen Aufbau und die Nutzung von JSON-Konfigurationsdateien für Profile und Validierungsregeln ist der **arkumu.nrw Import Assistant** flexibel erweiterbar.

---

## 5. Diskussion und kritische Reflexion
**Erfolge:**
- Schnelle Umsetzung dank Streamlit.  
- Intuitive Bedienbarkeit über die GUI.  
- Modularer Aufbau erleichtert zukünftige Erweiterungen.

**Einschränkungen:**
- Unterstützung nur für CSV-Dateien.  
- Keine automatische Fehlerkorrektur, nur Validierung.  
- Abhängigkeit von korrekt gepflegten JSON-Konfigurationsdateien.
- Benötigt als File-Upload noch vollständige CSV Datenpakete

**Nächste Schritte:**
- Erweiterung für weitere Profile (z. B. HfMT).  
- Integration automatischer Korrekturvorschläge.  
- Anbindung an institutionelle Datenrepositorien.  
- Mehrsprachigkeit (Deutsch/Englisch UI).
- Verarbeitung einzelner CSV-Dateien, statt ganze CSV-Exportpakete zu fordern

---

## 6. Fazit
Der **arkumu.nrw Import Assistant** stellt ein praxisnahes Werkzeug zur Überprüfung und Verbesserung der Metadatenqualität dar. Durch die Kontrolle von Vollständigkeit, Konsistenz und Validität unterstützt die App die zuverlässige Überführung heterogener Datenbestände in die neue Infrastruktur. Sie bietet den beteiligten Institutionen eine leicht zugängliche Möglichkeit, die Kompatibilität ihrer exportierten Metadaten vor dem Import in arkumu.nrw sicherzustellen. Dabei ist insbesondere die Pflege der JSON-Konfigurationsdateien zu berücksichtigen, da diese die Validierungsregeln und Profile festlegen und somit integraler Bestandteil des Prüfprozesses sind.

Gleichzeitig trägt die Anwendung zur Umsetzung der FAIR-Prinzipien bei und verdeutlicht die Bedeutung eines professionellen Metadaten- und Datenqualitätsmanagements im Kontext des Data Librarianship.

---

## Anhang  

### A.1 JSON-Beispielkonfiguration  
```json
"validation_targets": {
    "projekte": {
      "filename": "00_Projekte.csv",
      "required": [
        "Projekt_ID",
      ],
      "conditional": [
        {
          "if_filled": "Originaltitel",
          "then_required": ["Originaltitel_Sprache"]
        }
      ],
      "either_or": []
    },
```

### A.2 Code-Auszug `validation.py`
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
            missing_rows = df[
                df[if_col].notna() & (df[if_col].astype(str).str.strip() != "") &
                (df[then_col].isna() | (df[then_col].astype(str).str.strip() == ""))
            ]
            if not missing_rows.empty:
                conditional_errors.append(
                    extract_error_rows(
                        missing_rows,
                        [if_col, then_col],
                        f"{if_col} ausgefüllt, aber {then_col} leer"
                    )
                )
```

