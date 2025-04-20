
import openai

openai.api_key = "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"

def rota_olustur(gorevler):
    sehirler = [g["sehir"] for g in gorevler if g["durum"] == "beklemede"]
    if not sehirler:
        return "Bekleyen görev bulunamadı."

    prompt = (
        f"Aşağıdaki şehirleri Türkiye içi en kısa ve mantıklı ziyaret sırasına göre sırala:\n"
        f"{', '.join(sehirler)}\n"
        f"Başlangıç noktası Gebze olarak kabul edilmelidir."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
