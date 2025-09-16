# =============================================================
# validation.py
# Validierungslogik für CSV-Dateien inkl. Pflichtfelder, Conditional, Either/Or und Dubletten
# =============================================================

import pandas as pd

def check_duplicates(df: pd.DataFrame, subset=None) -> dict:
    """
    Prüft Dubletten in einem DataFrame.
    
    Args:
        df (pd.DataFrame): Zu prüfender DataFrame.
        subset (list, optional): Liste von Spalten, in denen Dubletten geprüft werden sollen.
                                 Wenn None, werden alle Spalten geprüft.
    Returns:
        dict: {"ok": bool, "errors": DataFrame}
    """
    dupes = df[df.duplicated(subset=subset, keep=False)]
    if dupes.empty:
        return {"ok": True, "errors": pd.DataFrame()}
    else:
        # Fehlerbeschreibung hinzufügen
        id_col = "Projekt_ID" if "Projekt_ID" in dupes.columns else dupes.columns[0]
        error_df = dupes[[id_col]].copy()
        error_df["Fehlerbeschreibung"] = "Dubletten gefunden"
        return {"ok": False, "errors": error_df}


def validate_dataframe(df: pd.DataFrame, rules: dict) -> dict:
    """
    Validiert ein DataFrame nach den Regeltypen:
    - Required: Pflichtfelder
    - Conditional: Abhängigkeiten zwischen Feldern
    - Either/Or: mindestens eines von mehreren Feldern muss gefüllt sein
    - Duplicates: Dubletten prüfen

    Gibt ein Dictionary zurück, das für jeden Regeltyp den Status ("ok") und
    die entsprechenden Fehlerzeilen enthält. Jede Fehlerzeile erhält eine
    zusätzliche Spalte 'Fehlerbeschreibung'.

    Args:
        df : pd.DataFrame
            Die zu validierenden Daten
        rules : dict
            JSON-artige Struktur mit den Regeln für Required, Conditional, Either/Or, Duplicates
    """
    
    # Ergebnis-Dictionary initialisieren
    result = {
        "required": {"ok": True, "errors": pd.DataFrame()},
        "conditional": {"ok": True, "errors": pd.DataFrame()},
        "either_or": {"ok": True, "errors": pd.DataFrame()},
        "duplicates": {"ok": True, "errors": pd.DataFrame()}
    }

    # -------------------
    # Hilfsfunktion: Fehlerzeilen extrahieren
    # -------------------
    def extract_error_rows(rows_df, cols, description):
        if rows_df.empty:
            return pd.DataFrame()
        id_col = "Projekt_ID" if "Projekt_ID" in rows_df.columns else rows_df.columns[0]
        error_df = rows_df[[id_col]].copy()
        error_df["Fehlerbeschreibung"] = description
        return error_df

    # -------------------
    # Required prüfen
    # -------------------
    required_cols = rules.get("required", [])
    missing_entries = []

    for col in required_cols:
        if col not in df.columns:
            missing_entries.append(pd.DataFrame({
                "Fehlende_Spalte": [col],
                "Fehlerbeschreibung": ["Spalte fehlt"]
            }))
        else:
            missing_rows = df[df[col].isnull() | (df[col].astype(str).str.strip() == "")]
            if not missing_rows.empty:
                missing_entries.append(extract_error_rows(missing_rows, [col], f"{col} fehlt"))

    if missing_entries:
        result["required"]["ok"] = False
        result["required"]["errors"] = pd.concat(missing_entries, ignore_index=True)

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

    if conditional_errors:
        result["conditional"]["ok"] = False
        result["conditional"]["errors"] = pd.concat(conditional_errors, ignore_index=True)

    # -------------------
    # Either/Or prüfen
    # -------------------
    either_or_rules = rules.get("either_or", [])
    either_or_errors = []

    for rule in either_or_rules:
        cols = rule.get("columns", [])
        existing_cols = [c for c in cols if c in df.columns]

        if not existing_cols:
            either_or_errors.append(pd.DataFrame({
                "Fehlende_Spalte": cols,
                "Fehlerbeschreibung": ["Spalte fehlt"] * len(cols)
            }))
            continue

        missing_rows = df[existing_cols].apply(
            lambda row: all(pd.isna(v) or str(v).strip() == "" for v in row),
            axis=1
        )

        if missing_rows.any():
            either_or_errors.append(extract_error_rows(
                df[missing_rows],
                existing_cols,
                f"Entweder {' oder '.join(existing_cols)} muss ausgefüllt sein"
            ))

    if either_or_errors:
        result["either_or"]["ok"] = False
        result["either_or"]["errors"] = pd.concat(either_or_errors, ignore_index=True)

    # -------------------
    # Dubletten prüfen
    # -------------------
    duplicate_columns = rules.get("duplicates", None)
    result["duplicates"] = check_duplicates(df, subset=duplicate_columns)

    return result