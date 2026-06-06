import os
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatOpenAI(model="gpt-4o", temperature=0.3)
parser = StrOutputParser()


prep_chain = {
    "orijinal_xeber": RunnablePassthrough(),
    "text": RunnablePassthrough()
}

# prep_chain = RunnablePassthrough.assign(
#     orijinal_xeber=lambda x: x["xeber"],
#     text=lambda x: x["xeber"]
# )


sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "Sən xəbər analitikisən. Xəbərin tonunu (Müsbət, Mənfi, Neytral) müəyyən et və 1 cümləlik izah yaz."),
    ("human", "{text}")
])
sentiment_chain = sentiment_prompt | model | parser

kateqoriya_prompt = ChatPromptTemplate.from_messages([
    ("system", "Xəbərin sahəsini tap (İqtisadiyyat, Siyasət, Texnologiya və s.) və confidence faizi (0-100%) qeyd et."),
    ("human", "{text}")
])
kateqoriya_chain = kateqoriya_prompt | model | parser

keywords_prompt = ChatPromptTemplate.from_messages([
    ("system", "Mətndən 3 ən vacib açar sözü çıxar, vergüllə ayır."),
    ("human", "{text}")
])
keywords_chain = keywords_prompt | model | parser

parallel_analysis = RunnableParallel(
    sentiment=sentiment_chain,
    kateqoriya=kateqoriya_chain,
    keywords=keywords_chain
)


def format_report(data: Dict) -> Dict:
    raw_sentiment = data['sentiment'].lower()
    emoji = "🟡"
    if "müsbət" in raw_sentiment:
        emoji = "🟢"
    elif "mənfi" in raw_sentiment:
        emoji = "🔴"

    return {
        "xeber_id": "XB-2026",
        "analiz": {
            "ton": f"{emoji} {data['sentiment'].split('.')[0]}",
            "izah": data['sentiment'],
            "sahə": data['kateqoriya'],
            "açar_sözlər": data['keywords'].split(',')
        },
        "status": "TAMAMLANDI"
    }


report_pipeline = parallel_analysis | RunnableLambda(format_report)

user_memories = {}


def get_session_history(session_id: str):
    if session_id not in user_memories:
        user_memories[session_id] = InMemoryChatMessageHistory()
    return user_memories[session_id]


chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Sən aşağıdakı analiz hesabatına cavabdeh mütəxəssissən:\n\n{analysis_report}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

chat_chain = chat_prompt | model | parser

final_system = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="user_input",
    history_messages_key="chat_history"
)


xeber_text = "Azərbaycan Mərkəzi Bankı uçot faizini 0.25% artırdı."
input_data = {"xeber": xeber_text}

prepped_data = prep_chain.invoke(input_data)
final_report = report_pipeline.invoke(prepped_data)

print(final_report)

config = {"configurable": {"session_id": "murad_01"}}

response1 = final_system.invoke(
    {"user_input": "Bu faiz artımı iqtisadiyyat üçün nə deməkdir?", "analysis_report": str(final_report)},
    config=config
)
print(f"AI: {response1}")

response2 = final_system.invoke(
    {"user_input": "Bayaq dediyim xəbərdə ton nə idi?", "analysis_report": str(final_report)},
    config=config
)
print(f"\nAI (Yaddaşlı): {response2}")