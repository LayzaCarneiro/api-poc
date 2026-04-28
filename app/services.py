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

# function to transform csv data into a cube format for 3D charts
def build_cube(rows, schema):

    categories = [c["name"] for c in schema if c["type"] == "category"]
    metrics = [c["name"] for c in schema if c["type"] == "metric"]

    x_col = categories[0]
    y_col = categories[1] if len(categories) > 1 else categories[0]
    z_col = categories[2] if len(categories) > 2 else categories[0]
    value_col = metrics[0]

    x_map = {}
    y_map = {}
    z_map = {}

    cells = []

    for row in rows:
        xv = row[x_col]
        yv = row[y_col]
        zv = row[z_col]

        if xv not in x_map:
            x_map[xv] = len(x_map)

        if yv not in y_map:
            y_map[yv] = len(y_map)

        if zv not in z_map:
            z_map[zv] = len(z_map)

        cells.append({
            "x": x_map[xv],
            "y": y_map[yv],
            "z": z_map[zv],
            "value": int(float(row[value_col]))
        })

    return cells