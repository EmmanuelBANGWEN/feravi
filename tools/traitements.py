import json
from datetime import datetime, timedelta

# Charger les données
with open('data.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

# Indexer les données par (date, time_slot)
data_map = {}
for entry in data:
    fields = entry['fields']
    key = (fields['date'], fields['time_slot'])
    data_map[key] = {
        'temperature': fields.get('temperature'),
        'humidity': fields.get('humidity'),
        'egg_count': fields.get('egg_count'),
        'chicken_count': fields.get('chicken_count'),
    }

def calculate_mean(target_date_str, time_slot, data_map):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    
    previous_dates = [
        (target_date - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, 11)
    ]

    temperature_values = []
    humidity_values = []
    egg_count_values = []
    chicken_count_values = []

    for d in previous_dates:
        key = (d, time_slot)
        if key in data_map:
            record = data_map[key]
            if record['temperature'] is not None:
                temperature_values.append(record['temperature'])
            if record['humidity'] is not None:
                humidity_values.append(record['humidity'])
            if record['egg_count'] is not None:
                egg_count_values.append(record['egg_count'])
            if record['chicken_count'] is not None:
                chicken_count_values.append(record['chicken_count'])

    # Calculer les moyennes
    def safe_mean(values):
        return round(sum(values) / len(values), 2) if values else None

    result = {
        'average_temperature': safe_mean(temperature_values),
        'average_humidity': safe_mean(humidity_values),
        'average_egg_count': safe_mean(egg_count_values),
        'average_chicken_count': safe_mean(chicken_count_values),
    }

    return result

# Exemple d'utilisation
target_day = "2025-04-23"
target_time_slot = "17:00"

averages = calculate_mean(target_day, target_time_slot, data_map)

print(f"Moyennes pour {target_day} à {target_time_slot} : {averages}")
