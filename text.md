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

Die Arbeit stellt den **arkumu.nrw Import Assistant** vor, eine in Python entwickelte Anwendung zur Validierung von Metadaten im Rahmen des Projekts arkumu.nrw. Die App überprüft aus Hochschularchiven exportierte CSV-Dateien auf Vollständigkeit, Konsistenz und Validität und stellt sie in einer benutzerfreundlichen Oberfläche dar. Damit ermöglicht sie eine effiziente Vorprüfung der Datenqualität und unterstützt die Anschlussfähigkeit an das arkumu.nrw-Datenmodell.

---

## 1. Einleitung und Kontext

Die Erschließung, Verfügbarhaltung und dauerhafte Archivierung multimedialer künstlerischer Bestände stellt Bibliotheken, Archive und Museen vor besondere Herausforderungen. Mit dem Projekt arkumu.nrw wird ein landesweites Portal geschaffen, das die qualitativ hochwertige Erschließung, Standardisierung und Archivierung der Bestände der Kunst- und Musikhochschulen Nordrhein-Westfalens bündelt. Ziel ist es, die digitalen Objekte und Metadaten der beteiligten Hochschulen in die Langzeitarchivierungsstrukturen des Landes NRW zu überführen und zugleich ihre wissenschaftliche, künstlerische und öffentliche Nutzung durch einheitliche Metadatenstandards und eine benutzerfreundliche Oberfläche zu fördern.

Die fünf beteiligten Kunst- und Musikhochschulen verfügen über sehr unterschiedliche Ausgangsbedingungen: Während einige bislang keine systematischen Archivierungsstrukturen aufgebaut haben und Daten auf lokalen Speichermedien ablegen, verwalten andere seit Jahrzehnten gewachsene Bestände in etablierten Datenbanksystemen. Um die heterogenen Ausgangslagen der beteiligten Hochschulen in eine gemeinsame Infrastruktur zu überführen, ist ein einheitliches Datenmodell notwendig, das verbindliche Pflichtfelder und konsistente Strukturen vorgibt. Die App setzt an dem Punkt an, an dem die Daten aus den Hochschularchiven exportiert werden: Sie ermöglicht Projektbeteiligten, diese CSV-Dateien vorab auf ihre Übereinstimmung mit dem arkumu.nrw-Datenmodell zu prüfen.

Dabei wird überprüft, ob alle erforderlichen Pflichtfelder ausgefüllt sind und die Daten strukturell kompatibel vorliegen. Auf diese Weise können Inkonsistenzen frühzeitig erkannt und behoben werden, sodass der anschließende Import in arkumu.nrw reibungslos und zuverlässig erfolgen kann.

Nach dieser vorbereitenden Validierung werden die Metadaten von den Projektbeteiligten in eine vom **IT Center University of Cologne (ITCC)** entwickelte Django-Anwendung überführt und anschließend von dort aus an das Hochschulbibliothekszentrum (`hbz`) sowie dessen Langzeitverfügbarkeitsstrukturen übergeben. Die App selbst ist damit nicht Teil des Importprozesses, sondern erfüllt die Funktion einer vorgeschalteten Qualitätssicherung: Sie bietet eine strukturierte Ansicht der Metadaten, überprüft die Erfüllung von Pflichtfeldern und stellt so sicher, dass die Daten zuverlässig für die weitere Verarbeitung vorbereitet sind.

---

## 2. Hintergrund und theoretische Grundlagen

Die Verarbeitung und Archivierung multimedialer Forschungs- und Kunstbestände erfordert eine hohe Datenqualität, um deren langfristige Verfügbarkeit und Nachnutzbarkeit sicherzustellen. Fehlende Pflichtangaben, uneinheitliche Schreibweisen oder inkonsistente Verknüpfungen führen schnell zu Inkompatibilitäten, die den Importprozess behindern oder Nacharbeiten erforderlich machen.

Zur Sicherstellung von Konsistenz und Anschlussfähigkeit wurden in arkumu.nrw [verbindliche Pflichtfelder](https://docs.arkumu.nrw/ressourcen/entitaeten-und-attribute-des-datenmodells) sowie ein [gemeinsames Datenmodell](https://docs.arkumu.nrw/ressourcen/einfuehrung-in-das-datenmodell.html) definiert. Die Überprüfung der Einhaltung dieser Vorgaben ist ein klassischer Anwendungsfall der Datenvalidierung, die als Teil des übergeordneten Datenqualitätsmanagements verstanden wird. Dabei umfasst die Validierung nicht nur die formale Prüfung auf ausgefüllte Felder, sondern auch die semantische Kontrolle von Abhängigkeiten und Konditionalitäten (z. B. „Wenn ein Projekt einen Projekttitel hat, muss auch eine Sprachauszeichnung des Projekttitels vorliegen“).

Für die technische Umsetzung existieren im Bereich der Datenvalidierung bereits verschiedene Ansätze und Tools, etwa Schema-Validierungen für XML oder JSON, Prüfroutinen in Datenbankmanagementsystemen oder Validierungsframeworks wie OpenRefine für tabellarische Daten. Im Kontext von arkumu.nrw reicht jedoch kein generisches Werkzeug aus, da die zu verarbeitenden Metadaten spezifischen fachlichen und strukturellen Anforderungen unterliegen, die durch ein maßgeschneidertes Validierungssystem abgedeckt werden müssen.

Die theoretische Grundlage der App orientiert sich zudem an den FAIR-Prinzipien (Findable, Accessible, Interoperable, Reusable), die als Leitlinie für den Umgang mit Forschungsdaten etabliert sind. Indem die App sicherstellt, dass Metadaten konsistent und standardkonform vorliegen, trägt sie unmittelbar zur Auffindbarkeit (Findability) und Interoperabilität bei und unterstützt langfristig die Nachnutzbarkeit (Reusability) relevanter Bestände.

---

## 3. Projektbeschreibung und Umsetzung

Im Rahmen der Arbeit wurde mit dem **arkumu.nrw Import Assistant** eine leichtgewichtige Web-Anwendung entwickelt, die den Validierungsprozess der Metadaten unterstützt. Sie ermöglicht Projektbeteiligten, die aus den Hochschularchiven exportierten CSV-Dateien auf Vollständigkeit, Konsistenz und Validität zu prüfen, bevor diese in arkumu.nrw importiert werden. Die App wurde in Python programmiert und nutzt das Framework **Streamlit**, das eine schnelle Entwicklung interaktiver Weboberflächen erlaubt.

Die Anwendung folgt einem klar strukturierten Ablauf: Zunächst wählen die Nutzer:innen ein Profil aus, das die jeweils geltenden Validierungsregeln lädt. Danach werden die für das Profil erforderlichen CSV-Dateien hochgeladen. Anschließend überprüft die App, ob alle erforderlichen Dateien vorhanden sind und ob die darin enthaltenen Pflichtfelder korrekt ausgefüllt wurden. Auch konditionale Abhängigkeiten zwischen Feldern werden automatisch geprüft, sodass beispielsweise beim Vorhandensein eines Originaltitels auch das entsprechende Sprachfeld ausgefüllt sein muss. Die Ergebnisse werden sowohl in einer kompakten Übersicht als auch in einer detaillierten tabellarischen Darstellung bereitgestellt. Eine direkte Bearbeitung der CSV-Dateien innerhalb der App ist nicht möglich, um die Integrität der Originaldaten zu gewährleisten.

Die Software ist modular aufgebaut: `app.py` steuert die Benutzeroberfläche und den Ablauf, während `utils.py` wiederverwendbare Funktionen zur Datenverarbeitung bereitstellt. Die Validierungslogik ist in `validation.py` gekapselt, die visuelle Darstellung der Ausgaben erfolgt über `views.py`. Projektspezifische Profile und Validierungsregeln sind in JSON-Dateien hinterlegt, die im Unterordner `configs` liegen; ein Beispiel hierfür ist in **Anhang A.1** zu finden. Die zentrale Funktion `validate_dataframe` überprüft die Daten zeilenweise anhand der in den JSON-Dateien definierten Regeln. 

Die Validierung differenziert dabei drei Regeltypen, um die unterschiedlichen Anforderungen des arkumu.nrw-Datenmodells präzise abzubilden: Zum einen **Required Rules**, die klassische Pflichtfelder darstellen und in jeder Zeile ausgefüllt sein müssen (z. B. `Projekt_ID` oder `Originaltitel`). Zum anderen **Conditional Rules**, bei denen das Ausfüllen eines Feldes automatisch das Vorhandensein weiterer, abhängiger Felder verlangt (z. B. das Feld *Originaltitel_Sprache*, wenn ein *Originaltitel* angegeben ist). Schließlich existieren **Either/Or Rules**, bei denen mindestens eines von mehreren Feldern befüllt sein muss (z. B. entweder ein *Eventanfangsdatum* oder ein *EventEnddatum*). Auf diese Weise lassen sich sowohl formale als auch semantische Konsistenzen prüfen, wodurch typische Fehlerquellen bei der Datenübertragung frühzeitig identifiziert werden. Eine exemplarische Anwendung der Funktion `validate_dataframe` für Conditional Rules ist in **Anhang A.2** dargestellt.

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
Die Entwicklung des Tools verlief insgesamt erfolgreich. Besonders positiv war die schnelle Umsetzbarkeit mit Streamlit, das eine ansprechende Oberfläche bei vergleichsweise geringem Aufwand ermöglicht. Auch die Nutzung von JSON-Konfigurationsdateien hat sich als sinnvoll erwiesen, da dadurch institutionelle Anpassungen leicht vorgenommen werden können.  

Dennoch bestehen Einschränkungen. Aktuell unterstützt das Tool nur CSV-Dateien und bietet keine Möglichkeit, erkannte Fehler automatisch zu korrigieren. Eine weitere Herausforderung besteht in der Abhängigkeit von korrekt gepflegten Konfigurationsdateien: Fehler in den JSON-Profilen können zu fehlerhaften Prüfungen führen.  

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

for rule in conditional_rules:
    if_col = rule.get("if_filled")
    then_cols = rule.get("then_required", [])
    if if_col in df.columns:
        for then_col in then_cols:
            if then_col not in df.columns:
                conditional_errors.append(pd.DataFrame({"Fehlende_Spalte": [then_col], "Fehlerbeschreibung": ["Spalte fehlt"]}))
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

