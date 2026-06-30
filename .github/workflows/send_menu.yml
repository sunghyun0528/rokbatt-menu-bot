import os
import requests
from datetime import datetime, timezone, timedelta

LEBANON_TZ = timezone(timedelta(hours=3))

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MEAL_TYPE = os.environ["MEAL_TYPE"]

def parse_menu():
    menu = {}
    current_date = None
    with open("menu.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if len(line) == 10 and line[4] == "-" and line[7] == "-":
                current_date = line
                menu[current_date] = {}
            elif current_date and ":" in line:
                meal, items = line.split(":", 1)
                meal = meal.strip()
                if meal in ["아침", "점심", "저녁"]:
                    menu[current_date][meal] = items.strip()
    return menu

def main():
    now = datetime.now(LEBANON_TZ)
    today = now.strftime("%Y-%m-%d")
    emoji = {"아침": "🌅", "점심": "☀️", "저녁": "🌙"}
    menu = parse_menu()

    if today not in menu or MEAL_TYPE not in menu[today]:
        msg = f"⚠️ {today} {MEAL_TYPE} 메뉴 정보 없음\nmenu.txt를 업데이트해주세요."
    else:
        items_raw = menu[today][MEAL_TYPE]
        # 쉼표로 나눠서 줄바꿈 처리
        items_list = [i.strip() for i in items_raw.split(",") if i.strip()]
        items_formatted = "\n".join(f"• {item}" for item in items_list)

        msg = (
            f"{emoji.get(MEAL_TYPE, '🍽')} <b>{MEAL_TYPE} 메뉴</b>\n"
            f"📅 {today}\n"
            f"──────────────\n"
            f"{items_formatted}\n"
            f"──────────────\n"
            f"맛있게 드세요! 😊"
        )

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    ).raise_for_status()
    print("✅ 전송 완료")

if __name__ == "__main__":
    main()
