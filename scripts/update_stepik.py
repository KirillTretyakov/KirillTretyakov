import os
from pathlib import Path

import requests


API_HOST = "https://" + "stepik.org"

CLIENT_ID = os.environ["STEPIK_CLIENT_ID"]
CLIENT_SECRET = os.environ["STEPIK_CLIENT_SECRET"]
USER_ID = os.environ["STEPIK_USER_ID"]


def get_access_token() -> str:
    response = requests.post(
        f"{API_HOST}/oauth2/token/",
        data={
            "grant_type": "client_credentials",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def get_user(token: str) -> dict:
    response = requests.get(
        f"{API_HOST}/api/users/{USER_ID}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data["users"][0]


def generate_svg(user: dict) -> str:
    knowledge = user.get("knowledge", 0)
    reputation = user.get("reputation", 0)

    return f"""
<svg
    width="500"
    height="170"
    viewBox="0 0 500 170"
    xmlns="http://www.w3.org/2000/svg"
>
    <style>
        .title {{
            font: 600 22px 'Segoe UI', Ubuntu, sans-serif;
            fill: #58a6ff;
        }}

        .label {{
            font: 400 15px 'Segoe UI', Ubuntu, sans-serif;
            fill: #8b949e;
        }}

        .value {{
            font: 600 18px 'Segoe UI', Ubuntu, sans-serif;
            fill: #c9d1d9;
        }}
    </style>

    <rect
        x="0.5"
        y="0.5"
        rx="8"
        width="499"
        height="169"
        fill="#0d1117"
        stroke="#30363d"
    />

    <text x="25" y="42" class="title">
        🎓 Stepik Stats
    </text>

    <text x="25" y="88" class="label">
        Knowledge
    </text>

    <text x="210" y="88" class="value">
        {knowledge}
    </text>

    <text x="25" y="125" class="label">
        Reputation
    </text>

    <text x="210" y="125" class="value">
        {reputation}
    </text>
</svg>
""".strip()


def main():
    token = get_access_token()

    user = get_user(token)

    print(
        "Available Stepik user fields:",
        sorted(user.keys()),
    )

    svg = generate_svg(user)

    output = Path("assets/stepik-stats.svg")
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(svg, encoding="utf-8")

    print("Stepik stats updated")


if __name__ == "__main__":
    main()