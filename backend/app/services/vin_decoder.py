from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


async def decode_vin(vin: str) -> dict[str, Any]:
    """Decode a VIN using an external provider (placeholder implementation)."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/',
            params={'format': 'json', 'vin': vin},
        )
        response.raise_for_status()
        data = response.json()
        return data.get('Results', [{}])[0]
