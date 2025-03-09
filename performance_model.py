import flet as ft

# Function to create the performance model tab
def performance_model_tab():
    performance_data = {
        "LSTM": {"Accuracy": 0.9995, "Precision": 0.9990, "Recall": 0.9995},
        "GRU": {"Accuracy": 0.9995, "Precision": 0.9990, "Recall": 0.9995},
        "ARIMA": {"MSE": 285.83, "RMSE": 16.91},
        "SARIMA": {
            "MSE (Upper)": 1707.73,
            "RMSE (Upper)": 41.32,
            "MSE (Lower)": 1503.55,
            "RMSE (Lower)": 38.78
        },
        "Random Forest (n=100)": {
            "Accuracy": 0.5876,
            "Precision": 0.5700,
            "Recall": 0.6000
        }
    }

    # Table 1: Accuracy, Precision, and Recall
    classification_table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Model")),
        ft.DataColumn(ft.Text("Accuracy")),
        ft.DataColumn(ft.Text("Precision")),
        ft.DataColumn(ft.Text("Recall")),
    ])

    for model_name, metrics in performance_data.items():
        if "Accuracy" in metrics:
            classification_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(model_name)),
                ft.DataCell(ft.Text(f"{metrics['Accuracy']:.4f}")),
                ft.DataCell(ft.Text(f"{metrics['Precision']:.4f}")),
                ft.DataCell(ft.Text(f"{metrics['Recall']:.4f}")),
            ]))

    # Table 2: ARIMA & SARIMA Error Metrics
    error_table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Model")),
        ft.DataColumn(ft.Text("Metric")),
        ft.DataColumn(ft.Text("Value")),
    ])

    for model_name, metrics in performance_data.items():
        if "MSE" in metrics or "MSE (Upper)" in metrics:
            for metric_name, value in metrics.items():
                error_table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(model_name)),
                    ft.DataCell(ft.Text(metric_name)),
                    ft.DataCell(ft.Text(f"{value:.2f}")),
                ]))

    # Return the UI layout
    return ft.Column([
        ft.Text("Model Performance Metrics", size=22, weight="bold"),
        ft.Text("Accuracy, Precision, and Recall", size=18, weight="bold"),
        classification_table,
        ft.Text("ARIMA & SARIMA Error Metrics", size=18, weight="bold"),
        error_table
    ], spacing=20)