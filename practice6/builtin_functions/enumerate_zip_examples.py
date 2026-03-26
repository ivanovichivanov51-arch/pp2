from functools import reduce

# Мәліметтер
names = ["Асхат", "Берік", "Анар", "Дәурен"]
scores = [85, 40, 90, 55]

# 1. filter(): Тек 60-тан жоғары балл алғандарды сүзу
high_scores = list(filter(lambda x: x > 60, scores))

# 2. map(): Барлық баллдарға 5 бонус қосу
bonus_scores = list(map(lambda x: x + 5, scores))

# 3. reduce(): Барлық баллдардың қосындысын табу
total_sum = reduce(lambda x, y: x + y, scores)

# 4. zip() және enumerate(): Есімдер мен баллдарды жұптастыру
print("\nСтуденттер тізімі:")
for i, (name, score) in enumerate(zip(names, scores), 1):
    print(f"{i}. {name}: {score} балл")

# 5. Типтерді тексеру және түрлендіру
сан_мәтін = "100"
if isinstance(сан_мәтін, str):
    нақты_сан = int(сан_мәтін)
    print(f"\nТүрлендірілген сан: {нақты_сан}, Типі: {type(нақты_сан)}")