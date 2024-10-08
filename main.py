import os
import time
from datetime import datetime

import dotenv

from i_ke import scraper
from i_ke import webhook


dotenv.load_dotenv()


def main():
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    IKE_URL = os.getenv("IKE_URL")
    message_id = os.getenv("MESSAGE_ID")
    change_detected = False

    while not change_detected:
        if not message_id:
            message_id = webhook.send_message(
                DISCORD_WEBHOOK_URL,
                title="starting...",
                description="I-KE 알리미 시작 중...",
                color=0x00FF00,
            )

        time.sleep(60)

        result = scraper.get_product_info(IKE_URL)
        update_time = datetime.now().strftime("%y-%m-%d %H:%M:%S")

        manual = result.get("manual", None)
        stock_button = result.get("stock_button", None)

        if not manual or not stock_button:
            title = "🔔 I-KE 알리미 🔔"
            info = f"❗ 입고 공지가 변경되거나, 상품이 입고되면 모두에게 알려드려요.\n\n🌐 [직접 확인하러 가기 <<< Click]({IKE_URL})"
            description = f"**\n✅ [실시간 감지 : Updated on {update_time}](https://github.com/hoonlight/i-ke)\n\n\n💬 현재 상태 : _구매 불가_\n\n📅 최근 공지 : _ 2/29(목) 12:00 재판매는..._\n\n\n{info}**"
            color = 0x00FF00 if not change_detected else 0xFFFF00
            webhook.edit_message(
                DISCORD_WEBHOOK_URL, message_id, title, description, color
            )
            time.sleep(60)
            continue

        if not stock_button == "구매 불가":
            change_detected = True

            info = f"🌐 [직접 확인하러 가기 <<< Click]({IKE_URL})"
            webhook.send_message(
                DISCORD_WEBHOOK_URL,
                title="",
                description=f"**\n⚠️ 구매 버튼 업데이트 감지!\n\n\n{info}**",
                mention=True,
                color=0xFFFF00,
            )

        if not manual.startswith("** 2/29(목) 12:00"):
            change_detected = True

            info = f"🌐 [직접 확인하러 가기 <<< Click]({IKE_URL})"
            webhook.send_message(
                DISCORD_WEBHOOK_URL,
                title="",
                description=f"**\n⚠️ 공지 업데이트 감지!\n\n\n{info}**",
                mention=True,
                color=0xFFFF00,
            )

        title = "🔔 I-KE 알리미 🔔"
        info = f"❗ 입고 공지가 변경되거나, 상품이 입고되면 모두에게 알려드려요.\n\n🌐 [직접 확인하러 가기 <<< Click]({IKE_URL})"
        description = f"**\n✅ [실시간 감지 : Updated on {update_time}](https://github.com/hoonlight/i-ke)\n\n\n💬 현재 상태 : _{stock_button}_\n\n📅 최근 공지 : _{manual.strip("* ")[:18]}..._\n\n\n{info}**"
        color = 0x00FF00 if not change_detected else 0xFFFF00
        webhook.edit_message(DISCORD_WEBHOOK_URL, message_id, title, description, color)


if __name__ == "__main__":
    print("starting...")
    main()
