import os, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

for model in ['qwen/qwen3.8-27b', 'openai/gpt-oss-20b', 'groq/compound']:
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Say hello in JSON format, like {"message": "hello"}'}],
            response_format={'type': 'json_object'}
        )
        print(f'{model} SUCCESS: ' + res.choices[0].message.content)
    except Exception as e:
        print(f'{model} FAILED: ' + str(e))
