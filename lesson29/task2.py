import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .env faylındakı API açarlarını sistemə tanıdırıq
load_dotenv()

#chaini ---> prompt,model,parser

model=ChatOpenAI(model="gpt-4o",temperature=0)

system_prompt="""
Sen bir musteri xidmetleri temsilcisisen.
Sene gelen problemleri analiz et ve nezaketli hell yonumlu cavablar teqdim et
Cavablarin resmi ve qisa olsun
"""

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{kategoriya},{sual}")
    ]
)

parser=StrOutputParser()

chain=prompt | model | parser

cavab=chain.invoke({"kategoriya":"TV","sual":"Tv-ni yandira bilmirem"})
print(cavab)