# main.py (only the /api/check-ip/{ip} route body needs to match this)

import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()
ANALYSIS_SERVICE_URL = os.getenv("ANALYSIS_SERVICE_URL", "http://analysis-service:8002").rstrip("/")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/check-ip/{ip}")
async def check_ip(ip: str):
    url = f"{ANALYSIS_SERVICE_URL}/check-ip"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            # IMPORTANT: pass the ip the user entered
            r = await client.get(url, params={"ip": ip})
        r.raise_for_status()
        data = r.json()

        # Normalize keys so frontend gets country & provider reliably
        return {
            "query": data.get("query", ip),
            "reputation": data.get("reputation", "Unknown"),
            "country": data.get("country") or data.get("country_name") or data.get("countryCode"),
            "provider": data.get("provider") or data.get("isp"),
            "isp": data.get("isp") or data.get("provider"),
            "threats": data.get("threats", []),
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to analysis service: {e}")
