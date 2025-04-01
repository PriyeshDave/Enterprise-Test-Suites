from openai import OpenAI  
from config import OPENAI_API_KEY, MODEL_NAME

class LLMClient:
    def __init__(self):
        self.api_key = OPENAI_API_KEY

    def query_llm(self, prompt: str) -> str:
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[{"role": "system", "content": "You are an expert in API testing and automation."},
                      {"role": "user", "content": prompt}]
        )

        response_content = response.choices[0].message.content.strip()
        return response_content
