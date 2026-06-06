import os
from dotenv import load_dotenv
from langchain_core import chat_history
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnableWithMessageHistory, RunnablePassthrough
from scipy._lib.pyprima.common import history
from sqlalchemy.ext.asyncio import result

load_dotenv()


model=ChatOpenAI(model="gpt-4o")

parser=StrOutputParser()

# prompt=ChatPromptTemplate.from_messages(
#     [
#         ("system","Sən HR mütəxəssisisən. Vakansiyadan yalnız texniki bacarıqları (skills) siyahı kimi çıxar."),
#         ("human","{job_description}")
#     ]
# )
#
# chain= { "job_description": RunnablePassthrough()} | prompt | model | parser
#
# skills=chain.invoke({"job_description":"Python ve Django bilen Senior Developer axtarilir"})
#
# print(skills)




# prompt1=ChatPromptTemplate.from_messages(
#     [
#         ("system","Vakansiyanın çətinlik dərəcəsini müəyyən et (Asan/Orta/Çətin)"),
#         ("human","{text}")
#     ]
# )
#
# chain1=prompt1 | model | parser
#
# prompt2=ChatPromptTemplate.from_messages(
#     [
#         ("system","Vakansi ucun 1 cumlelik muraciet metni yaz"),
#         ("human","{text}")
#     ]
# )
# chain2=prompt2 | model | parser
#
#
# paralel_analysis=RunnableParallel(
#     derece=chain1,
#     muraciet=chain2
# )
#
#
# def change(data):
#     yeni_derece=data['derece'].upper().strip()
#     yeni_muraciet=data['muraciet'].upper()
#
#     return {
#         "status":"ugurlu",
#         "derece":yeni_derece,
#         "muraciet":yeni_muraciet
#     }
#
# result=paralel_analysis | RunnableLambda(change)
#
# son_cavab=result.invoke({"text":"Senior Data Scientist axtarilir,5 il tecrube,3000+maas"})
# print(son_cavab)



memory={}

def get_memory(session_id:str):
    if session_id not in memory:
        memory[session_id]=InMemoryChatMessageHistory()
    return memory[session_id]

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Sen bir AI komekcisen"),
        ("placeholder","{chat_history}"),
        ("human","{user_input}")
    ]
)

chain=prompt | model | parser

history=RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="user_input",
    history_messages_key="chat_history",
)

config={"configurable":{"session_id":"gulnar"}}
config2={"configurable":{"session_id":"ali"}}

sual1=history.invoke({"user_input":"Salam,menim adim Gulnardir ve Python bilirem"},config=config)
sual2=history.invoke({"user_input":"Menim adim nedir ve ne bilirem"},config=config)
sual3=history.invoke({"user_input":"Menim adim nedir ve ne bilirem"},config=config2)
print("Sual1: ",sual1,"\nSual2: ",sual2,"\nSual3: ",sual3)