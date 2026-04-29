import json
import os

# Файлдардың толық жолын анықтау
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """Файлдың нақты жолын қайтарады"""
    return os.path.join(BASE_DIR, filename)

def load_json(filename, default):
    """Файлды жүктейді, егер файл жоқ болса — әдепкі мәнді қайтарады"""
    path = get_path(filename)
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default

def save_json(filename, data):
    """Мәліметтерді JSON форматында сақтайды"""
    path = get_path(filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# --- Лидерборд функциялары ---
def get_leaderboard():
    """Топ-10 ұпайлар тізімін алу"""
    return load_json('leaderboard.json', [])

def save_score(name, score, distance):
    """Жаңа нәтижені сақтау және топ-10-ды жаңарту [cite: 17, 18]"""
    lb = get_leaderboard()
    lb.append({
        "name": name, 
        "score": score, 
        "distance": int(distance)
    })
    # Ұпайы бойынша сорттап (ең жоғарыдан төмен), тек алғашқы 10-ын қалдыру [cite: 18]
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    save_json('leaderboard.json', lb)

# --- Баптаулар (Settings) функциялары ---
def get_settings():
    """Ойын баптауларын жүктеу [cite: 22]"""
    default_settings = {
        "sound": True, 
        "car_color": "Red", 
        "difficulty": "Medium"
    }
    return load_json('settings.json', default_settings)

def save_settings(settings):
    """Ойын баптауларын сақтау [cite: 22]"""
    save_json('settings.json', settings)