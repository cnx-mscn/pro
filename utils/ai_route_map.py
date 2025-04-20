import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rota_olustur(tasks):
    sehirler = [t["sehir"] for t in tasks if "sehir" in t]
    prompt = "Şehirler: " + ", ".join(sehirler) + ". En uygun rota sıralaması nedir?"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir rota planlama asistanısın."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
