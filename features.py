import os
from datetime import datetime
import random

def analyze_personality():
    return "شما فردی مهربان، صادق و جست‌وجوگر هستید."

def analyze_dream():
    return "خواب شما نشانه‌ای از استرس‌های روزمره و تمایل به تغییر است."

def zodiac_sign(day, month):
    zodiacs = {
        (1, 20): ("Capricorn", "صبر، سخت‌کوشی"),
        (2, 19): ("Aquarius", "خلاق، اجتماعی"),
        (3, 21): ("Pisces", "مهربان، خیالباف"),
        (4, 20): ("Aries", "انرژیک، شجاع"),
        (5, 21): ("Taurus", "واقع‌گرا، وفادار"),
        (6, 21): ("Gemini", "دوگانه، باهوش"),
        (7, 23): ("Cancer", "احساسی، خانواده‌دوست"),
        (8, 23): ("Leo", "رهبری، بااعتماد"),
        (9, 23): ("Virgo", "منطقی، تحلیل‌گر"),
        (10, 23): ("Libra", "متعادل، مهربان"),
        (11, 22): ("Scorpio", "مرموز، قدرتمند"),
        (12, 22): ("Sagittarius", "جسور، ماجراجو"),
    }
    for (m, d), (z, desc) in zodiacs.items():
        if month == m and day <= d:
            return z, desc
    return "Capricorn", "صبر، سخت‌کوشی"

def countdown_to_100(day, month, year):
    today = datetime.now()
    birth = datetime(year, month, day)
    age = today.year - birth.year
    remaining = 100 - age
    return f"⌛️ تا ۱۰۰ سالگی {remaining} سال باقی مانده."

async def save_user_info(user, bot):
    os.makedirs("data", exist_ok=True)
    with open("data/users.txt", "a") as f:
        f.write(str(user.id) + "\n")

def generate_motivation():
    motivations = [
        "هر روز یک فرصت جدیده برای بهتر شدن!",
        "با تلاش مداوم، به هدف‌هات می‌رسی.",
        "مثبت فکر کن، زندگی بهتر میشه.",
        "موفقیت نتیجه تلاش و صبر است.",
        "امروز بهترین روز برای شروع دوباره است."
    ]
    return random.choice(motivations)
