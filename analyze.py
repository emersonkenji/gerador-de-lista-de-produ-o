import pandas as pd
import json

file_path = "Export_Order20260409214937.xlsx"
try:
    df = pd.read_excel(file_path)
    output = {
        "columns": list(df.columns),
        "first_rows": df.head(5).to_dict(orient="records")
    }
    with open("analyze_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print("Success")
except Exception as e:
    print("Failed with pandas, error:", e)
    import traceback
    traceback.print_exc()
