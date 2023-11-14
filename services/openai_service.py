import traceback

import aiohttp
import backoff

from services.environment_service import EnvService
from services.prompts.image_analysis_prompt import IMAGE_ANALYSIS_PROMPT


def backoff_handler_request(details):
    print(
        f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries calling function {details['target']} | "
        f"{details['exception'].args[0]}"
    )

class OpenAIExecutor:

    def __init__(self):
        self.openai_api_key = EnvService.get_openai_api_key()
        try:
            self.ANALYSIS_PRETEXT = IMAGE_ANALYSIS_PROMPT
        except Exception:
            traceback.print_exc()
            self.ANALYSIS_PRETEXT = "Describe this image in as much detail as you can, for the visually impaired."

    @backoff.on_exception(
        backoff.expo,
        ValueError,
        factor=3,
        base=5,
        max_tries=4,
        on_backoff=backoff_handler_request,
    )
    async def send_image_evaluation_request(
        self,
        image_urls,
    ):
        messages = [
            {"role": "system", "content": self.ANALYSIS_PRETEXT}
        ]
        for image_url in image_urls:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
                    ]
                }
            )

        async with aiohttp.ClientSession(
            raise_for_status=False, timeout=aiohttp.ClientTimeout(total=300)
        ) as session:
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": messages,
                "temperature": 0,
                "max_tokens": 2048,
            }

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}"
            }

            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
            ) as resp:
                response = await resp.json()
                # print(f"Payload -> {payload}")
                # Parse the total tokens used for this request and response pair from the response
                print(f"Response -> {response}")

                return response["choices"][0]["message"]["content"]

