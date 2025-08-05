import asyncio
import os

import httpx


async def main():
    MEDIDA_API_BASE_URL = os.environ["MEDIDA_API_BASE_URL"]
    MEDIDA_API_KEY = os.environ["MEDIDA_API_KEY"]

    http_client = httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {MEDIDA_API_KEY}",
        }
    )

    response = await http_client.get(f"{MEDIDA_API_BASE_URL}/v1/projects/csv")
    if response.is_error:
        raise RuntimeError(response.text)

    with open("projects.csv", "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    asyncio.run(main())
