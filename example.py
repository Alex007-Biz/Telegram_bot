from openai import OpenAI
from config2 import OPEN_API_K


client = OpenAI(api_key=OPEN_API_K)


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write an invitation to birthday."
        }
    ]
)

print(completion.choices[0].message)
