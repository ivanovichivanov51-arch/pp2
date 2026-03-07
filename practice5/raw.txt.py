import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


prices = re.findall(r"\d+\.\d{2}", text)

print("Барлық бағалар:")
print(prices)


total = sum(float(price) for price in prices)

print("Жалпы сома:", total)


date = re.search(r"\d{4}-\d{2}-\d{2}", text)
time = re.search(r"\d{2}:\d{2}", text)

if date:
    print("Күні:", date.group())

if time:
    print("Уақыты:", time.group())
    
    
    
payment = re.search(r"Payment Method:\s*(\w+)", text)

if payment:
    print("Төлем әдісі:", payment.group(1))
    
    
import json

data = {
    "prices": prices,
    "total": total,
    "date": date.group() if date else None,
    "time": time.group() if time else None,
    "payment_method": payment.group(1) if payment else None
}

print("\nJSON Output:")
print(json.dumps(data, indent=4))


