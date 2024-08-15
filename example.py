from openai import OpenAI
from config import OA_KEY


client = OpenAI(api_key=OA_KEY)


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
