
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def öneri_üret(görevler_listesi):
    if not görevler_listesi:
        return "Henüz görev geçmişi yok. Öneri yapılamaz."

    görevler = [f"{g['sehir']} - {g['gorev_adi']} - {g['tarih']}" for g in görevler_listesi]

    prompt = (
        "Aşağıda geçmişte tamamlanmış bazı montaj görevleri verilmiştir:\n"
        + "\n".join(görevler) +
        "\nBu verilere dayanarak önerilecek yeni görevleri listele."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
