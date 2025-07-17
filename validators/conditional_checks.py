def check_conditional_required_columns(df, conditional_rules):
    report = {}

    for rule in conditional_rules:
        if_col = rule.get("if_filled")
        then_cols = rule.get("then_required", [])

        if if_col not in df.columns:
            report[if_col] = "Spalte fehlt für Bedingungsprüfung"
            continue

        for then_col in then_cols:
            if then_col not in df.columns:
                report[then_col] = "Spalte fehlt als Pflichtfeld"
                continue

            # Zeilen finden, bei denen Bedingung verletzt wird
            missing_rows = df[
                (df[if_col].notnull()) & (df[if_col] != "") &  # if_filled ist befüllt
                ((df[then_col].isnull()) | (df[then_col] == ""))  # then_required fehlt
            ]

            if not missing_rows.empty:
                report[f"{then_col} (wenn {if_col} gesetzt)"] = len(missing_rows)

    return report