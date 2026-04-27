import os

import tiktoken
from IPython.core.magics import history
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

numuneli_mesajlar = [
    {
        "role": "system",
        "content": "Sən xəbərləri analiz edən köməkçisən. Hər xəbər başlığı üçün yalnız Kateqoriya və Vaciblik formatında cavab ver."
    },
    {
        "role": "user",
        "content": "Apple yeni süni intellekt çipini təqdim etdi."
    },
    {
        "role": "assistant",
        "content": "Kateqoriya: Texnologiya\nVaciblik: 9"
    },
    {
        "role": "user",
        "content": "Qarabağ futbol klubu növbəti qələbəsini qazandı."
    },
    {
        "role": "assistant",
        "content": "Kateqoriya: İdman\nVaciblik: 7"
    },
    {
        "role": "user",
        "content": "Yeni kosmik gəmi Marsa eniş etdi."
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=numuneli_mesajlar,
    max_tokens=256
)

print(response.choices[0].message.content)

# def test_et():
#     prompt = "Bakı şəhəri haqqında qısa, bədii bir cümlə yaz."
#
#     print("--- DETERMINISTIK TEST (Temp=0) ---")
#     for i in range(3):
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             max_tokens=100,
#             temperature=0,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         print(f"{i+1}-ci cəhd: {response.choices[0].message.content}")
#
#     print("\n--- YARADICI TEST (Temp=1.0) ---")
#     for i in range(3):
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             max_tokens=100,
#             temperature=1.0,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         print(f"{i+1}-ci cəhd: {response.choices[0].message.content}")
#
# test_et()

#
# history=[{"role":"system","content":"Sən bir Python Müəllimisən,suallara cavab ver"}]
#
# def cavab(istifadeci_mesaj):
#     history.append({"role":"user","content":istifadeci_mesaj})
#
#     cavab = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=1000,
#         messages=history
#     )
#
#     ai_cavab=cavab.choices[0].message.content
#     history.append({"role":"assistant","content":ai_cavab})
#     return ai_cavab
#
#
# print(cavab("List nədir"))
# print("-------------")
# print(cavab("Ona aid nümunə göstər"))
#



#
# cavab=client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=1000,
#     messages=
#     [
#         {"role":"system",
#          "content":"Sən bir Python Müəllimisən,suallara cavab ver"
#         },
#         {"role":"user",
#          "content":"Python nədir?"
#
#         }
#     ]
# )
# print(cavab.choices[0].message.content)


# enc=tiktoken.encoding_for_model("gpt-4o")
#
# metn="Tiktoken istifade ede bilirem"
#
# tokenler=enc.encode(metn)
#
# print(tokenler)
# print(len(tokenler))
#
# for t in tokenler:
#     print(repr(enc.decode([t])))