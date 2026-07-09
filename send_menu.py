import os
import requests
from datetime import datetime, timezone, timedelta

LEBANON_TZ = timezone(timedelta(hours=3))

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MEAL_TYPE = os.environ["MEAL_TYPE"]

PAGES_BASE_URL = "https://rokbatt.github.io/rokbatt-menu-bot"

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
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"현재 시각(레바논): {now}")
    print(f"오늘 날짜: {today}")
    print(f"MEAL_TYPE: {MEAL_TYPE}")

    emoji = {"아침": "🌅", "점심": "☀️", "저녁": "🌙"}
    menu = parse_menu()
    print(f"파싱된 날짜 목록: {list(menu.keys())}")

    if today not in menu or MEAL_TYPE not in menu[today]:
        print(f"매칭 실패 - today in menu: {today in menu}")
        msg = f"⚠️ {today} {MEAL_TYPE} 메뉴 정보 없음\nmenu.txt를 업데이트해주세요."
        reply_markup = None
    else:
        items_raw = menu[today][MEAL_TYPE]
        items_list = [i.strip() for i in items_raw.split(",") if i.strip()]
        items_formatted = "\n".join(f"• {item}" for item in items_list)

        msg = (
            f"{emoji.get(MEAL_TYPE, '🍽')} {MEAL_TYPE} 메뉴\n"
            f"📅 {today}\n"
            f"──────────────\n"
            f"{items_formatted}\n"
            f"──────────────\n"
            f"맛있게 드세요! 😊"
        )

        if MEAL_TYPE == "저녁":
            btn_text = "📅 내일 식단표 보기"
            btn_url = f"{PAGES_BASE_URL}?date={tomorrow}"
        else:
            btn_text = "📅 오늘 식단표 보기"
            btn_url = f"{PAGES_BASE_URL}?date={today}"

        reply_markup = {
            "inline_keyboard": [[
                {"text": btn_text, "url": btn_url}
            ]]
        }

    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json=payload
    )
    print(f"응답 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")
    response.raise_for_status()
    print("전송 완료")

if __name__ == "__main__":
    main()
