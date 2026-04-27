import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SISTEM_PROMPT = """
Sən 'AzərTravel' agentliyinin professional turizm köməkçisən.
Məhdudiyyətlər:
- Yalnız Bakı, Gəncə və Şəki şəhərləri haqqında məlumat verirsən. Başqa yer soruşulsa: "Xidmət dairəmiz hələlik yalnız Azərbaycanın bu üç şəhərini əhatə edir" de.
- Hər cavabda əvvəlki söhbətdən qalan büdcəni nəzərə almalı, riyazi hesablamalar aparmalı və yeni qalan məbləği göstərməlisən.
- Cavab formatın mütləq belə olmalıdır:
  DÜŞÜNCƏ: [Riyazi hesablamalar və məntiqi analiz]
  CAVAB: [Müştəriyə nəzakətli təklif]
  QALAN BÜDCƏ: [Rəqəm] AZN
"""

sobet_tarixi = [
    {"role": "system", "content": SISTEM_PROMPT},
    # Nümunə 1: Uğurlu ssenari
    {"role": "user", "content": "Bakıda 1 gün, büdcə 100 AZN."},
    {"role": "assistant",
     "content": "DÜŞÜNCƏ: Bakı daxili nəqliyyat və yemək təxminən 50 AZN tutur. 100 AZN kifayətdir.\nCAVAB: İçərişəhər və Bulvar gəzintisi təklif edirəm.\nQALAN BÜDCƏ: 50 AZN"},
    # Nümunə 2: İmtina ssenarisi
    {"role": "user", "content": "İstanbul üçün plan ver."},
    {"role": "assistant",
     "content": "DÜŞÜNCƏ: İstanbul xidmət dairəmdə deyil.\nCAVAB: Xidmət dairəmiz hələlik yalnız Azərbaycanın bu üç şəhərini (Bakı, Gəncə, Şəki) əhatə edir.\nQALAN BÜDCƏ: 0 AZN"}
]


def seyahat_agenti_islet(sual):
    sobet_tarixi.append({"role": "user", "content": sual})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=sobet_tarixi,
            temperature=0
        )

        model_cavabi = response.choices[0].message.content
        sobet_tarixi.append({"role": "assistant", "content": model_cavabi})

        return model_cavabi
    except Exception as e:
        return f"Xəta baş verdi: {e}"


def start_chat():
    print("--- AzərTravel Agentliyinə Xoş Gəlmisiniz! ---")
    print("(Çıxmaq üçün 'exit' yazın)\n")

    while True:
        istifadeci_suali = input("Siz: ")

        if istifadeci_suali.lower() == 'exit':
            print("Səyahətiniz uğurlu keçsin! Sağ olun.")
            break

        print("\nAgent düşünür...")
        cavab = seyahat_agenti_islet(istifadeci_suali)

        print(f"\n{cavab}")
        print("-" * 40)


if __name__ == "__main__":
    start_chat()