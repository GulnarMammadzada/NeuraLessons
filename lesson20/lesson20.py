import os
from html import parser
from itertools import chain
from urllib import parse

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()


model=ChatOpenAI(model="gpt-4o",temperature=0.5)


prompt=ChatPromptTemplate.from_messages(

    [
        ("system","Sen bir avtomobil mutexessisisen,cavabi json formatinda ver"),
        ("human","{marka} xususiyyetlerini yaz.Bu saheler olsun:il,model_adi,gucu")
    ]
)

parser=JsonOutputParser()

chain= prompt | model | parser

ai_cavab=chain.invoke({"marka":"Toyota Camry"})
print(ai_cavab)
print(ai_cavab['il'])
print(ai_cavab['model_adi'])
print(ai_cavab['gucu'])

# mesajlar=[
#     {"olke":"Italiya","sual":"En meshur yemeyi nedir?"},
#     {"olke":"fransa","sual":"Eyfel qullesi nece metrdir?"},
#     {"olke":"Fransa","sual":"piramidlari kim tikib"}
# ]
#
# ai_cavab=chain.batch(mesajlar)
#
# for c in ai_cavab:
#     print(c)


# ai_cavab=chain.stream()
#
# for c in ai_cavab:
#     print(c,end="",flush=True)

# prompt=PromptTemplate(
#     input_variables=["mehsul","xususiyyet"],
#     template="Sen {mehsul} ucun reklam menti hazirlayirsan.Esas {xususiyyet} xususiyyetini vurgula"
# )
#
# hazir_prompt=prompt.format(mehsul="saat",xususiyyet="suya davamlilig")
# print(hazir_prompt)
#
