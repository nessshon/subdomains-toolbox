import json
from typing import Optional

import cachetools
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from image_generator import generate_image

SUPPORTED_TLD = ["ton"]

app = FastAPI(include_in_schema=False)

# 24-hour cache for up to 1000 generated images
cache = cachetools.TTLCache(maxsize=1000, ttl=86400)


@cachetools.cached(cache)
def get_cached_image(domain: str, tld: str, subdomain: Optional[str] = None) -> bytes:
    return generate_image(domain, subdomain, tld)


def validate_tld_or_400(tld: str) -> None:
    if tld not in SUPPORTED_TLD:
        raise HTTPException(status_code=400, detail="Unsupported TLD")


def generate_image_response(domain: str, tld: str, subdomain: Optional[str] = None) -> Response:
    try:
        image = get_cached_image(domain, tld, subdomain)
        return Response(content=image, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/{tld}/{domain}.png", include_in_schema=False)
async def image_without_subdomain(tld: str, domain: str) -> Response:
    validate_tld_or_400(tld)
    return generate_image_response(domain, tld)


@app.get("/api/{tld}/{subdomain}/{domain}.png", include_in_schema=False)
async def image_with_subdomain(tld: str, subdomain: str, domain: str) -> Response:
    validate_tld_or_400(tld)
    return generate_image_response(domain, tld, subdomain)


@app.get("/api/{tld}/{subdomain}/{domain}.json", include_in_schema=False)
async def metadata_handler(
        tld: str,
        subdomain: str,
        domain: str
) -> Response:
    validate_tld_or_400(tld)
    try:
        metadata = {
            "description": (
                f"A .{domain}.{tld} blockchain domain. "
                f"TON DNS is a service that allows users to assign a human-readable name "
                f"to crypto wallets, smart contracts, and websites."
            ),
            "attributes": [
                {
                    "trait_type": "length",
                    "value": str(len(subdomain)),
                }
            ]
        }
        return Response(
            content=json.dumps(metadata, ensure_ascii=False, indent=2),
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
