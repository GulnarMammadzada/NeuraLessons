from openai import OpenAI

client = OpenAI(    api_key="Your_Api_Key")
budce=input("Budce")
kategoriya=input("Kategoriya")


system_prompt=f"""
Budece:{budce},"kategoriya:{kategoriya}
"""

user_prompt="""
Dunen telefon aldim,1 hefte isledi sonra gordum donur,
duzeltmek istedim alinmadi,Mecbur apardim ustaya duzeltdi.
Qiymetine gore superdi amma kash daha islek olardi
"""


history=[
    {"role":"system",
     "content":system_prompt}
]

while(True):
    rey=input("Reyinizi daxil edin:")
    history.append({
        "role":"user",
        "content":rey
    })

    response=client.chat.completions.create(
        model="gpt-4o",
        messages=history
    )

    ai_cavab=response.choices[0].message.content
    print(ai_cavab)


    history.append({
        "role":"assistant",
        "content":ai_cavab
    })

