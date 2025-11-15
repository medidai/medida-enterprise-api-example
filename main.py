import asyncio
import os
from uuid import UUID

import httpx


def _parse_filename(response_headers: httpx.Headers) -> str | None:
    content_disposition = response_headers.get("content-disposition")
    if content_disposition is None:
        return None

    parts = content_disposition.split("filename=")
    if len(parts) != 2:
        return None

    return parts[1].strip('"')


async def get_all_projects_csv(
    http_client: httpx.AsyncClient,
) -> None:
    response = await http_client.get("/enterprise/v1/projects/csv")
    if response.is_error:
        raise RuntimeError(response.text)

    output_filename = _parse_filename(response.headers) or "projects.csv"
    with open(output_filename, "w") as f:
        f.write(response.text)


async def get_project_csv_by_id(
    http_client: httpx.AsyncClient,
    project_id: UUID,
) -> None:
    response = await http_client.get(f"/enterprise/v1/projects/{project_id}/csv")
    if response.is_error:
        raise RuntimeError(response.text)

    output_filename = _parse_filename(response.headers) or f"project-{project_id}.csv"
    with open(output_filename, "w") as f:
        f.write(response.text)


async def get_project_photos_by_id(
    http_client: httpx.AsyncClient,
    project_id: UUID,
) -> None:
    response = await http_client.get(f"/enterprise/v1/projects/{project_id}/photos")
    if response.is_error:
        raise RuntimeError(response.text)

    output_filename = (
        _parse_filename(response.headers) or f"project-photos-{project_id}.zip"
    )
    with open(output_filename, "wb") as f:
        f.write(response.content)


async def main():
    MEDIDA_API_BASE_URL = os.environ["MEDIDA_API_BASE_URL"]
    MEDIDA_API_KEY = os.environ["MEDIDA_API_KEY"]

    http_client = httpx.AsyncClient(
        base_url=MEDIDA_API_BASE_URL,
        headers={"Authorization": f"Bearer {MEDIDA_API_KEY}"},
    )

    # Get CSV of all projects.
    await get_all_projects_csv(http_client=http_client)

    # Get CSV of a specific project with more details.
    await get_project_csv_by_id(
        http_client=http_client,
        # You can find the UUID of a project in the all projects CSV file.
        project_id=UUID("af2cfdc3-f4be-4d3b-bd3a-33f816b621b8"),
    )

    # Get photos of a specific project.
    await get_project_photos_by_id(
        http_client=http_client,
        # You can find the UUID of a project in the all projects CSV file.
        project_id=UUID("af2cfdc3-f4be-4d3b-bd3a-33f816b621b8"),
    )


if __name__ == "__main__":
    asyncio.run(main())
