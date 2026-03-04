import json
import re
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.AI_API_KEY)


def analyze_with_gemini(image):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = """
        Identify the Indian cattle or buffalo breed in this image, if the image contains a clearly visible Indian cattle or buffalo if not return invalid and not a cattle return unknown.

        Return ONLY valid JSON:
        {
            "breed": "Breed Name" - the name of the identified breed, such as "Gir", "Sahiwal", "Red Sindhi", "Murrah Buffalo", "Jersey", or "Holstein Friesian". If the breed cannot be confidently identified, retry and return "Unknown". Do not return any other text or explanations, only the breed name or "Unknown". The breed name should be exactly as listed above, without any additional words or descriptions.
            "type": "Cattle or Buffalo",
            "confidence": 0-100 - important: confidence should be a number between 0 and 100, representing the percentage confidence of the prediction, and should not be a decimal or a string. For example, if the confidence is 85.5%, it should be returned as 85, and if it's 90%, it should be returned as 90." and make default as 90 if confidence is not provided or is invalid.
        }
        """

        response = model.generate_content([prompt, image])

        text = response.text

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None

        data = json.loads(match.group())

        return {
            "breed": data.get("breed", "Unknown"),
            "type": data.get("type", "Cattle"),
            "confidence": float(data.get("confidence", 0))
        }

    except Exception as e:
        print("Gemini API Error:", e)
        return None
