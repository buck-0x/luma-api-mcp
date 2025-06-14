import asyncio
import os
import random

import aiohttp

base_url = "https://api.lumalabs.ai"
max_sleep_time_for_polling = 1  # seconds

headers = {
    "Authorization": f"Bearer {os.getenv('LUMA_API_KEY')}",
}


async def submit_image(
    body: dict,
    session: aiohttp.ClientSession,
):
    async with session.post(
        f"{base_url}/dream-machine/v1/generations/image",
        json=body,
        headers=headers,
    ) as response:
        return await response.json()


async def submit_video(
    body: dict,
    session: aiohttp.ClientSession,
):
    async with session.post(
        f"{base_url}/dream-machine/v1/generations",
        json=body,
        headers=headers,
    ) as response:
        return await response.json()


async def get_generation(id: str, session: aiohttp.ClientSession):
    async with session.get(
        f"{base_url}/dream-machine/v1/generations/{id}",
        headers=headers,
    ) as response:
        return await response.json()

async def list_generations(
    session: aiohttp.ClientSession,
    offset: int | None = 0,
    limit: int | None = 10,
):
    params = {
        "offset": offset,
        "limit": limit,
    }
    async with session.get(
        f"{base_url}/dream-machine/v1/generations",
        headers=headers,
        params=params,
    ) as response:
        return await response.json()


async def delete_generation(id: str, session: aiohttp.ClientSession):
    async with session.delete(
        f"{base_url}/dream-machine/v1/generations/{id}",
        headers=headers,
    ) as response:
        return await response.json()


async def get_completed_image(id: str, session: aiohttp.ClientSession) -> str:
    generation = await get_generation(id=id, session=session)
    status = generation.get("status", None)
    assets = generation.get("assets", {})
    if not isinstance(assets, dict):
        assets = {}
    image_url = assets.get("image", None)

    final_statuses = ["completed", "failed"]
    has_image = False

    while status in final_statuses or not has_image:
        await asyncio.sleep(random.random() * max_sleep_time_for_polling)
        generation = await get_generation(id=id, session=session)
        status = generation.get("status", None)
        if status == "failed":
            raise ValueError("Failed to get image from API response")
        assets = generation.get("assets", {})
        if not isinstance(assets, dict):
            assets = {}
        image_url = assets.get("image", None)
        has_image = image_url is not None

    return image_url


async def get_completed_video(id: str, session: aiohttp.ClientSession) -> dict:
    generation = await get_generation(id=id, session=session)
    status = generation.get("status", None)
    assets = generation.get("assets", {})
    if not isinstance(assets, dict):
        assets = {}
    image_url = assets.get("image", None)
    video_url = assets.get("video", None)

    final_statuses = ["completed", "failed"]
    has_image = False
    has_video = False

    while status in final_statuses or not has_image or not has_video:
        await asyncio.sleep(random.random() * max_sleep_time_for_polling)
        generation = await get_generation(id=id, session=session)
        status = generation.get("status", None)
        if status == "failed":
            raise ValueError("Failed to get image from API response")
        assets = generation.get("assets", {})
        if not isinstance(assets, dict):
            assets = {}
        image_url = assets.get("image", None)
        video_url = assets.get("video", None)
        has_image = image_url is not None
        has_video = video_url is not None

    return {
        "video": video_url,
        "image": image_url,
        "id": id,
    }


async def ping(session: aiohttp.ClientSession):
    async with session.get(
        f"{base_url}/dream-machine/v1/ping",
        headers=headers,
    ) as response:
        return await response.json()
async def get_credits(session: aiohttp.ClientSession):
    async with session.get(
        f"{base_url}/dream-machine/v1/credits",
        headers=headers,
    ) as response:
        return await response.json()
async def get_concepts(
    session: aiohttp.ClientSession,
    offset: int | None = 0,
    limit: int | None = 10,
):
    params = {
        "offset": offset,
        "limit": limit,
    }
    async with session.get(
        f"{base_url}/dream-machine/v1/concepts",
        headers=headers,
        params=params,
    ) as response:
        return await response.json()

from .types import ExtendRequest, ReframeRequest, UpscaleRequest


async def upscale_generation(id: str, payload: UpscaleRequest, session: aiohttp.ClientSession):
    async with session.post(
        f"{base_url}/dream-machine/v1/generations/{id}/upscale",
        json=payload.dict(),
        headers=headers,
    ) as response:
        return await response.json()


async def extend_generation(id: str, payload: ExtendRequest, session: aiohttp.ClientSession):
    async with session.post(
        f"{base_url}/dream-machine/v1/generations/{id}/extend",
        json=payload.dict(),
        headers=headers,
    ) as response:
        return await response.json()


async def reframe_generation(id: str, payload: ReframeRequest, session: aiohttp.ClientSession):
    async with session.post(
        f"{base_url}/dream-machine/v1/generations/{id}/reframe",
        json=payload.dict(),
        headers=headers,
    ) as response:
        return await response.json()
