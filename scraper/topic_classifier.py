import os
from openai import OpenAI
from typing import Optional

client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    api_key=os.getenv('OPENAI_API_KEY'),
    project=os.getenv('OPENAI_PROJECT_ID'),
)

SYSTEM_PROMPT = """
You will be given the lyrics to a song.
Based on these lyrics, respond with one word that represents the song's subject matter.
Make sure the topic is in English, even if the song lyrics are in a different language.
"""

def generate_topic(lyrics: str) -> (str, Optional[str]):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": lyrics}
            ]
        )
        return completion.choices[0].message.content, None

    except Exception as error:
        return "", str(error)