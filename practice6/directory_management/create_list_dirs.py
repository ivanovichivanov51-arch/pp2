import os

# 1. Сатылы (nested) бумалар құру
os.makedirs("projects/python_practice", exist_ok=True)

# 2. Бума ішіндегі файлдарды тізімдеу
print("Ағымдағы бумадағы файлдар:", os.listdir("."))

# 3. Кеңейтілімі бойынша файлдарды табу (мысалы, тек .txt)
files = [f for f in os.listdir(".") if f.endswith(".txt")]
print("Табылған мәтіндік файлдар:", files)