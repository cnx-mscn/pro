import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("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"))

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
