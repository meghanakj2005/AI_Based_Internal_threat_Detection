def generate_alerts(df):

    threats = df[df["Anomaly"] == "Threat"]

    alerts = []

    for _, row in threats.iterrows():

        alert = f"""
        Employee {row['employee_id']} suspicious activity:
        Login Hour: {row['login_hour']}
        Download: {row['download_mb']} MB
        """

        alerts.append(alert)

    return alerts