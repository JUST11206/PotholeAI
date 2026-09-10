import json

from google import genai
from google.genai import types

from config import Config
from services.priority_service import calculate_priority


client = genai.Client(
    api_key=Config.GEMINI_API_KEY
)


def analyze_pothole(image_path):

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    prompt = """
You are an AI road inspection system.

Analyze this road image specifically for potholes.

Return ONLY valid JSON in exactly this format:

{
    "detected": true,
    "confidence": 0.95,
    "severity": "high",
    "description": "Large pothole visible on the road"
}

Rules:

1. detected must be true or false.
2. confidence must be between 0 and 1.
3. severity must be one of:
   low, medium, high, critical
4. If there is no pothole:
   detected = false
   confidence should represent your confidence that no pothole exists.
5. Do not identify unrelated objects as potholes.
6. Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            ),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    result = json.loads(response.text)

    if not result["detected"]:
        return {
            "detected": False,
            "confidence": result["confidence"],
            "description": result.get(
                "description",
                ""
            )
        }

    score, priority = calculate_priority(
        severity=result["severity"],
        confidence=float(
            result["confidence"]
        )
    )

    return {
        "detected": True,
        "confidence": float(
            result["confidence"]
        ),
        "severity": result["severity"],
        "description": result.get(
            "description",
            ""
        ),
        "priority_score": score,
        "priority": priority
    }