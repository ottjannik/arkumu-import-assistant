# Zentrale Definition aller Regeln

required_columns = {
    "projekte": ["Projekt_ID", "Originaltitel", "Originaltitel_Sprache", "Projektart_calc", "Projektkategorien_arkumu"],
    "grundereignis": ["arkumu_Typ_Grundereignis", "Entstehungsjahr", "Entstehungsland"]
}

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