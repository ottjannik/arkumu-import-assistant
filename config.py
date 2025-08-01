# Alle globalen Konstanten, required files, Spaltenlisten

# Liste benötigter Dateien, die hochgeladen werden müssen um alle Funktionen des Dashboards zu nutzen
required_files = [
    "00_Projekte.csv",
    "01_Grundereignis.csv",
    "02_Kreuz_Projekte_Personen.csv",
    "03_Personen_Akteurinnen.csv",
    "04_Kreuz_Betreuende_Projekte.csv",
    "05_PersonenBetreuende.csv",
    "06_Auszeichnungen_Projekte.csv",
    "07_Kreuz_Projekte_Keywords.csv",
    "08_Keywords.csv",
    "09_Kreuz_Projekte_Informationsträger.csv",
    "10_PhysMedien_Informationstraeger.csv",
    "11_Kreuz_DigitaleObjekte_Proj.csv",
    "12_Media_DigitaleObjekte.csv",
    "16_Kreuz_Events_Projekte.csv",
    "17_Events_weitereEreignisse.csv",
    "18_Kreuz_Projekte_EquipmentSoftware.csv",
    "19_Equipment_und_Software.csv",
    "20_Equipmentart.csv",
    "21_PhysischesObjekt.csv"
]

# Prüfe auf Angaben in Spaten, die verpflichtend benötigt werden
required_columns = {
    "projekte": [
        "Projekt_ID",
        "Originaltitel",
        "Originaltitel_Sprache",
        "Projektart_calc",
        "Projektkategorien_arkumu",
    ],
    "grundereignis": [
        "arkumu_Typ_Grundereignis",
        "Entstehungsjahr",
        "Entstehungsland",
    ],
    "akteurinnen": [
        "Name_gesamt_natürlicheReihenfolge",
    ],
    "betreuende": [
        "Name_gesamt_natürlicheReihenfolge",
    ],
    "auszeichnungen": [
        "Ausz_Proj_ID",
        "Ereignistyp",
        "Ausz_Anfang",
    ],
    "keywords": [
        "Wikidata_QID",
        "Keyword_eng",
        "Keyword_deu",
    ],
}

# Prüfe auf Angaben in Spalten, die basierend auf der Existenz anderer Spalten verpflichtend benötigt werden
conditional_required_columns = {
    "projekte": [
        {"if_filled": "Untertitel", "then_required": "Untertitel_Sprache"},
        {"if_filled": "Titel_erster_alternativer_Titel", "then_required": "Titel_erster_alternativer_Titel_Sprache"},
        {"if_filled": "Titel_erster_alternativer_Untertitel", "then_required": "Titel_erster_alternativer_Untertitel_Sprache"},
        {"if_filled": "Titel_zweiter_alternativer_Titel", "then_required": "Titel_zweiter_alternativer_Titel_Sprache"},
        {"if_filled": "Titel_zweiter_alternativer_Untertitel", "then_required": "Titel_zweiter_alternativer_Untertitel_Sprache"},
    ],
    "grundereignis": [
        {"if_filled": "Entstehungsland", "then_required": "Entstehungs_und_Produktionsland_verkettet"}
    ]
}