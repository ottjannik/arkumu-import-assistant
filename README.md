# arkumu.nrw Import Assistant

arkumu.nrw Import Assistant ist eine Streamlit-Webanwendung, die Institutionen dabei unterstützt, ihre Metadaten vor dem Import in die Plattform arkumu.nrw zu überprüfen.

Die App stellt sicher, dass exportierte Metadaten vollständig, konsistent und valide sind, bevor sie auf arkumu.nrw hochgeladen werden.

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

## Starten der App
```bash
streamlit run app.py
```

## Benötigte CSV-Dateien
- 00_Projekte.csv
- 01_Grundereignis.csv
- 02_Kreuz_Projekte_Personen.csv
- 03_Personen_Akteurinnen.csv
- 04_Kreuz_Betreuende_Projekte.csv
- 05_PersonenBetreuende.csv
- 06_Auszeichnungen_Projekte.csv
- 07_Kreuz_Projekte_Keywords.csv
- 08_Keywords.csv
- 09_Kreuz_Projekte_Informationsträger.csv
- 10_PhysMedien_Informationstraeger.csv
- 11_Kreuz_DigitaleObjekte_Proj.csv
- 12_Media_DigitaleObjekte.csv
- 16_Kreuz_Events_Projekte.csv
- 17_Events_weitereEreignisse.csv
- 18_Kreuz_Projekte_EquipmentSoftware.csv
- 19_Equipment_und_Software.csv
- 20_Equipmentart.csv
- 21_PhysischesObjekt.csv
```
