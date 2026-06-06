from fontTools.misc.cython import returns
from openai import OpenAI
import tiktoken

from openai import OpenAI

client = OpenAI(
    api_key="Your_Api_Key"
)


System_Prompt="""
Sen bir muellimsen.8-10 yasli usaqlara ders deyirsen.
Sene verilen  qisa ve aydin usaqlarin basa duseceyi sekilde cavab ver,
Azerbaycan dilinde olsun

"""

numune1=client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"user",
         "content":"Fotosintez nedir?"}
    ]
)

cavab1=numune1.choices[0].message.content
print(cavab1)
print("--"*50)
numune2=client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role":"system",
            "content":System_Prompt
        }
        ,{"role":"user",
         "content":"Fotosintez nedir?"}
    ]
)
cavab2=numune2.choices[0].message.content
print(cavab2)






# System_Prompt="""
# wefgES
#
# """
#
#
#
# response=client.chat.completions.create(
#     model="gpt-4o",
#     temperature=0.5,
#     max_tokens=600,
#     messages=
#     [
#         {
#             "role":"system",
#             "content":System_Prompt
#         },
#         {
#             "role":"user",
#             "content":"Python nedir?"
#         }
#     ]
# )
#
#
# print(response.choices[0].message.content)
#
#
#
#
#





#
# encoder=tiktoken.encoding_for_model("gpt-4o")
#
#
# text="Ai proqramlasdirma"
#
#
# tokenler=encoder.encode(text)
#
# print(tokenler)
# for token in tokenler:
#     # print(token)
#     print(encoder.decode([token]))
#     print("-------------------------")
#     print(repr(encoder.decode([token])))



# messages=[
#         {
#             "role":"system",
#             "content":System_Prompt
#         }
#         ,{"role":"user",
#          "content":"Fotosintez nedir?"}
#     ]