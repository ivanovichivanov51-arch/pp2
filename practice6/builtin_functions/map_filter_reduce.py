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