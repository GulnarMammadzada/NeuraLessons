from langchain_community import vectorstores
from langchain_text_splitters import CharacterTextSplitter
from nbformat import v3

from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_classic.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from torch.distributed.tensor.parallel import input_reshard

load_dotenv()
client = OpenAI()


#
# def get_embedding(text:str) -> list[float]:
#
#     response=client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#
#     # print(response.data[0].embedding)
#     # print(len(response.data[0].embedding))
#     return response.data[0].embedding
#
#
# def calculate_similarity(vector1,vector2):
#
#      a=np.array(vector1)
#      b=np.array(vector2)
#      return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#
#
# v1=get_embedding("Pyton bilirem ve proqlasdirma oyrenirem")
# v2=get_embedding("Java bilirem ve python oyrenirem")
# v3=get_embedding("Men biznes sahesindeyem")
#
# sim1=calculate_similarity(v1,v2)
# sim2=calculate_similarity(v1,v3)
# sim3=calculate_similarity(v2,v3)
# print(sim1)
# print(sim2)
# print(sim3)

#
# get_embedding(" ")
# get_embedding("""Modern Texnologiya Akademiyası" Bakı şəhəri, Cəfər Cabbarlı küçəsi 44 ünvanında yerləşir. Akademiyada "Python Backend" (6 ay) və "Data Science" (8 ay) kursları tədris olunur. "Python Backend" kursunun aylıq ödənişi 300 AZN, "Data Science" isə 400 AZN-dir. Tələbələr dərslərə həm əyani, həm də onlayn qoşula bilərlər.""")


#
# text="Bakida hava cox gozeldir ve insanlar parkda gezir"
#
# splitter=CharacterTextSplitter(
#     separator=" ",
#     chunk_size=30,
#     chunk_overlap=15
# )
#
# chunks=splitter.split_text(text)
# for i,chunk in enumerate(chunks):
#     print(i,chunk)



#
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#
# # Sənədlər — real proyektdə bunlar fayldan oxunacaq
# documents = [
#     Document(
#         page_content="Refund politikası: 30 gün ərzində tam geri qaytarma mümkündür.",
#         metadata={"source": "policy.pdf"}  # sənədin haradan gəldiyi
#     ),
#     Document(
#         page_content="Çatdırılma müddəti: Bakı üçün 1-2 iş günü.",
#         metadata={"source": "shipping.pdf"}
#     ),
#     Document(
#         page_content="Əlaqə: info@company.az, iş saatları 09:00-18:00.",
#         metadata={"source": "contact.pdf"}
#     ),
# ]
#
# vectorstore=Chroma.from_documents(
#     documents=documents,
#     embedding=embeddings,
#     persist_directory="./my-chroma-db"
# )
#
# result=vectorstore.similarity_search(
#     query="Mehsulu nece qaytarim",
#     k=2
# )
#
#
# for doc in result:
#     print(doc.page_content)
#     print(doc.metadata['source'])



# memory = ConversationBufferMemory(
#     return_messages=True,
#     memory_key="history"
# )
#
# # Əl ilə məlumat əlavə etmək
# memory.chat_memory.add_user_message("Mənim adım Əlidir")
# memory.chat_memory.add_ai_message("Salam Əli!")
# memory.chat_memory.add_user_message("Bakıda yaşayıram")
# memory.chat_memory.add_ai_message("Bakı gözəl şəhərdir!")
#
# # Yaddaşın içini bax
# saved = memory.load_memory_variables({})
# for msg in saved["history"]:
#     print(f"{msg.type}: {msg.content}")




#
# from langchain_openai import ChatOpenAI
# from langchain_classic.chains import ConversationChain
# from langchain_classic.memory import ConversationBufferMemory
#
# # 1. Modelin yaradılması
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
#
# # 2. Yaddaşın yaradılması
# # 'history' açar sözü modelin keçmişi hara yazacağını müəyyən edir
# memory = ConversationBufferMemory()
#
# # 3. Zəncirin (Chain) qurulması
# # ConversationChain avtomatik olaraq yaddaşla LLM-i birləşdirir
# conversation = ConversationChain(
#     llm=llm,
#     memory=memory,
#     verbose=True  # Bu, pərdəarxasında yaddaşın necə işlədiyini görməyə imkan verir
# )
#
# # 4. Söhbət silsiləsi
# print(conversation.predict(input="Salam, mənim adım Əlidir."))
# # Bot cavab verir: "Salam Əli, səninlə tanış olmağıma şadam!"
#
# print(conversation.predict(input="Mən Bakıda yaşayıram."))
# # Bot cavab verir: "Bakı möhtəşəm şəhərdir!"
#
# print(conversation.predict(input="Mənim adım nədir və mən harada yaşayıram?"))
# # Bot yaddaş sayəsində cavab verir: "Sənin adın Əlidir və sən Bakıda yaşayırsan."
#





from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


# 1. ADDIM: Azərbaycanca mətni hazırlamaq və Chunking (Parçalamaq)
metn = """
Süni İntellekt Tədris Mərkəzi haqqında məlumat:
Mərkəzimiz Bakı şəhərində, Nizami küçəsi 45 ünvanında yerləşir.
Bizim əsas kursumuz "LLM və RAG Proqramlaşdırma" kursudur. 
Bu kurs 12 həftə davam edir və dərslər həftədə 2 dəfə keçirilir.
Kursun qiyməti 500 AZN-dir. Tələbələrə ödənişdə 2 hissəli güzəşt edilir.
Əlaqə nömrəmiz: +994 50 123 45 67.
"""

# Mətni parçalara bölürük
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)
chunks = text_splitter.split_text(metn)
# Mətnləri Document obyektinə çeviririk
docs = [Document(page_content=x) for x in chunks]

# 2. ADDIM: Indexing (Vektora çevirib Chroma-da saxlamaq)
# Qeyd: OpenAI API açarınızın sistemdə təyin olunduğundan əmin olun
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./mini_rag_db"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. ADDIM: Memory (Yaddaş) quraşdırılması
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="history"
)

# 4. ADDIM: RAG Chain və Chat funksiyası
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompt-u hazırlayırıq (Yaddaş və Kontekst daxil olmaqla)
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Sən köməkçi bir asistansan. Yalnız verilən kontekstdən istifadə edərək cavab ver.\n\nKontekst:\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])


def format_docs(found_docs):
    return "\n\n".join(d.page_content for d in found_docs)


# Chat funksiyası (İpucundakı struktura uyğun)
def chat(sual: str) -> str:
    # 1. Uyğun sənədləri tapırıq
    found_docs = retriever.invoke(sual)
    context = format_docs(found_docs)

    # 2. Tarixçəni yaddaşdan alırıq
    history = memory.load_memory_variables({})["history"]

    # 3. Zənciri (Chain) işə salırıq
    chain = prompt | llm | StrOutputParser()
    cavab = chain.invoke({
        "context": context,
        "history": history,
        "question": sual
    })

    # 4. Söhbəti yaddaşa yazırıq
    memory.save_context({"input": sual}, {"output": cavab})

    return cavab


# 5. TEST: 3 dövrlü söhbət
print("--- Söhbət Başlayır ---")

# 1-ci sual
q1 = "Kursun müddəti nə qədərdir?"
print(f"Sual: {q1}")
print(f"Cavab: {chat(q1)}\n")

# 2-ci sual
q2 = "Qiyməti neçədir?"
print(f"Sual: {q2}")
print(f"Cavab: {chat(q2)}\n")

# 3-cü sual (Əvvəlki cavaba istinad edir - Memory testi)
q3 = "Bəs ödənişi necə edə bilərəm? Yuxarıda dediyin qiyməti hissəli ödəmək olar?"
print(f"Sual: {q3}")
print(f"Cavab: {chat(q3)}\n")

