import httpx


def send_message(
    url: str, title: str, description: str, color: int, mention: bool = False
) -> str:
    try:
        params = {"wait": True}
        response = httpx.post(
            url,
            params=params,
            json={
                "content": "@everyone" if mention else "",
                "embeds": [
                    {"title": title, "description": description, "color": color}
                ],
            },
        )
        message_id = response.json().get("id")
        print(f"Message sent successfully with id: {message_id}")
    except Exception as e:
        print(e)
        message_id = None

    return message_id


def edit_message(
    url: str,
    message_id,
    title: str,
    description: str,
    color: int,
) -> None:
    try:
        httpx.patch(
            url=f"{url}/messages/{message_id}",
            json={
                "embeds": [
                    {"title": title, "description": description, "color": color}
                ],
            },
        )
    except Exception as e:
        print(e)
