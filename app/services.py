import pandas as pd

def detect_schema(df):
    columns = []

    metric_count = 0
    category_count = 0

    for col in df.columns:
        dtype = str(df[col].dtype)

        if "int" in dtype or "float" in dtype:
            col_type = "metric"
            metric_count += 1
        else:
            col_type = "category"
            category_count += 1

        columns.append({
            "name": col,
            "type": col_type
        })

    chart = suggest_chart(metric_count, category_count)

    return columns, chart


def suggest_chart(metrics, categories):
    if metrics == 1 and categories >= 1:
        return "bar3d"
    elif metrics >= 3:
        return "scatter3d"
    elif metrics == 2:
        return "bubble3d"
    return "grid3d"