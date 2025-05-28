from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

OPENROUTER_API_KEY = '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'  # store this in your settings.py

@csrf_exempt
def chatbot_apii(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Prepare request to OpenRouter
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct",  # Or try 'openchat/openchat-3.5'
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant for a jewelry ecommerce site."},
                        {"role": "user", "content": user_message}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
            )

            response_json = response.json()

            if response.status_code != 200 or 'choices' not in response_json:
                return JsonResponse({
                    "error": response_json.get('error', {}).get('message', 'Unknown error'),
                    "details": response_json
                }, status=500)

            bot_reply = response_json['choices'][0]['message']['content']
            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)