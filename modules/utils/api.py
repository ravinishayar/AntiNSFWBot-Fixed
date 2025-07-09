import httpx

async def isNsfw(file_path: str) -> bool:
    try:
        API_URL = "https://api.example.com/nsfw-detect"  # Replace with real API
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = await client.post(API_URL, files=files)
                if response.status_code == 200:
                    result = response.json()
                    return result.get("nsfw", False)
                else:
                    print(f"⚠️ API Error: {response.status_code}")
    except Exception as e:
        print(f"❌ API Request Failed: {e}")
    return False
