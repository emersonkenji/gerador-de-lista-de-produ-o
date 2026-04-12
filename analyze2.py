import pandas as pd
import json

file_path = "Export_Order20260412175524.xlsx"
try:
    df = pd.read_excel(file_path)
    output = {
        "columns": list(df.columns),
        "total_rows": len(df),
        "first_rows": df.head(10).to_dict(orient="records"),
        "unique_ads": df["Nome do Anúncio"].unique().tolist() if "Nome do Anúncio" in df.columns else [],
        "unique_variations": df["Variação"].unique().tolist() if "Variação" in df.columns else [],
        "unique_stores": df["Nome da Loja no UpSeller"].unique().tolist() if "Nome da Loja no UpSeller" in df.columns else [],
    }
    with open("analyze_output2.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print("Success -", len(df), "rows")
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
