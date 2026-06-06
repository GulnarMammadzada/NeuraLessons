from langchain_text_splitters import CharacterTextSplitter
#
# # 1. Sənədi yükləyirik (Məsələn, bir şirkət nizamnaməsi)
# text = "Bakı şəhərində hava çox gözəldir və insanlar parklarda gəzməyi çox sevirlər."
#
# # 2. Bölücü (Splitter) yaradırıq
# text_splitter = CharacterTextSplitter(
#     separator=" ",        # Mətni nəyə görə bölək? (Yeni sətir)
#     chunk_size=30,         # Hər parça maksimum neçə simvol olsun?
#     chunk_overlap=15       # Parçalar arasında keçid üçün neçə simvol üst-üstə düşsün?
# )
#
# # 3. Mətni parçalayırıq
# chunks = text_splitter.split_text(text)
# # print(f"Parça sayı: {len(chunks)}")
# for i, chunk in enumerate(chunks):
#     print(f"Hissə {i+1} (Uzunluq: {len(chunk)}):")
#     print(f"'{chunk}'")
#     print("-" * 20)





from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# client = OpenAI()
#
# def get_embedding(text: str) -> list[float]:
#     response = client.embeddings.create(
#         model="text-embedding-3-small",  # OpenAI-nin embedding modeli
#         input=text
#     )
#     # Nəticə 1536 ədəddən ibarət siyahıdır
#     return response.data[0].embedding
#
# embedding = get_embedding("Pişik evdə oturur")
# print(f"Vektor uzunluğu: {len(embedding)}")  # 1536
# print(f"İlk 5 ədəd: {embedding[:5]}")        # [-0.02, 0.14, ...]


# import numpy as np
# from openai import OpenAI
#
# client = OpenAI()
#
# def get_embedding(text: str) -> list[float]:
#     """Mətni 1536 ölçülü vektora çevirir"""
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding
#
# def calculate_similarity(vec1, vec2):
#     """İki vektor arasındakı oxşarlığı hesablayır (1.0 = eyni məna)"""
#     a = np.array(vec1)
#     b = np.array(vec2)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#
# # 1. Test üçün cümlələrimiz
# cumle1 = "Mənim pişiyim divanda yatır."
# cumle2 = "Kitti hazırda divanın üstündə yuxulayır." # Eyni məna, fərqli sözlər
# cumle3 = "Sabah Bakıda hava yağmurlu olacaq."    # Tamamilə fərqli mövzu
#
# # 2. Vektorları alırıq
# print("Vektorlar hesablanır...")
# v1 = get_embedding(cumle1)
# v2 = get_embedding(cumle2)
# v3 = get_embedding(cumle3)
#
# # 3. Müqayisə edirik
# sim_1_2 = calculate_similarity(v1, v2)
# sim_1_3 = calculate_similarity(v1, v3)
#
# print("-" * 30)
# print(f"Cümlə 1: '{cumle1}'")
# print(f"Cümlə 2: '{cumle2}'")
# print(f"Cümlə 3: '{cumle3}'")
# print("-" * 30)
# print(f"1 və 2 arasındakı oxşarlıq: {sim_1_2:.4f} (YÜKSƏK)")
# print(f"1 və 3 arasındakı oxşarlıq: {sim_1_3:.4f} (AŞAĞI)")
#



#
#

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
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
# # Sənədləri vektora çevirib Chroma-ya yazırıq
# vectorstore = Chroma.from_documents(
#     documents=documents,
#     embedding=embeddings,
#     persist_directory="./my_chroma_db"  # diskdə saxlanır
# )
#
# # Axtarış
# results = vectorstore.similarity_search(
#     query="məhsulu necə qaytarmaq olar?",
#     k=2  # ən oxşar 2 nəticə
# )
#
# for doc in results:
#     print(f"Tapildi: {doc.page_content}")
#     print(f"Mənbə: {doc.metadata['source']}")
#     print("---")
#

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
#
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#
# # Retriever: vectorstore-u axtarış aləti kimi işlədən interfeys
# retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
#
# # RAG üçün prompt
# rag_prompt = ChatPromptTemplate.from_template("""
# Aşağıdakı kontekstə əsasən suala cavab ver.
# Kontekstdə olmayan məlumatı uydurma.
#
# Kontekst:
# {context}
#
# Sual: {question}
#
# Cavab:
# """)
#
# def format_docs(docs: list) -> str:
#     # Tapılan sənədləri bir mətnə birləşdir
#     return "\n\n".join(doc.page_content for doc in docs)
#
# # RAG chain: sual → retrieval → prompt → LLM → cavab
# rag_chain = (
#     {
#         "context": retriever | format_docs,  # sual retriever-ə gedir
#         "question": RunnablePassthrough()    # sual olduğu kimi ötürülür
#     }
#     | rag_prompt
#     | llm
#     | StrOutputParser()
# )
#
# cavab = rag_chain.invoke("məhsulumu necə qaytara bilərəm?")
# print(cavab)
#





#
from langchain_classic.memory import ConversationBufferMemory
#
# # Bütün söhbəti saxlayır
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








# import os
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import Chroma
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain_classic.memory import ConversationBufferMemory
# from langchain_core.output_parsers import StrOutputParser
#
# # 1. ADDIM: Azərbaycanca mətni hazırlamaq və Chunking (Parçalamaq)
# metn = """
# Süni İntellekt Tədris Mərkəzi haqqında məlumat:
# Mərkəzimiz Bakı şəhərində, Nizami küçəsi 45 ünvanında yerləşir.
# Bizim əsas kursumuz "LLM və RAG Proqramlaşdırma" kursudur.
# Bu kurs 12 həftə davam edir və dərslər həftədə 2 dəfə keçirilir.
# Kursun qiyməti 500 AZN-dir. Tələbələrə ödənişdə 2 hissəli güzəşt edilir.
# Əlaqə nömrəmiz: +994 50 123 45 67.
# """
#
# # Mətni parçalara bölürük
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=150,
#     chunk_overlap=20
# )
# chunks = text_splitter.split_text(metn)
# # Mətnləri Document obyektinə çeviririk
# docs = [Document(page_content=x) for x in chunks]
#
# # 2. ADDIM: Indexing (Vektora çevirib Chroma-da saxlamaq)
# # Qeyd: OpenAI API açarınızın sistemdə təyin olunduğundan əmin olun
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# vectorstore = Chroma.from_documents(
#     documents=docs,
#     embedding=embeddings,
#     persist_directory="./mini_rag_db"
# )
# retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
#
# # 3. ADDIM: Memory (Yaddaş) quraşdırılması
# memory = ConversationBufferMemory(
#     return_messages=True,
#     memory_key="history"
# )
#
# # 4. ADDIM: RAG Chain və Chat funksiyası
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#
# # Prompt-u hazırlayırıq (Yaddaş və Kontekst daxil olmaqla)
# prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      "Sən köməkçi bir asistansan. Yalnız verilən kontekstdən istifadə edərək cavab ver.\n\nKontekst:\n{context}"),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{question}")
# ])
#
#
# def format_docs(found_docs):
#     return "\n\n".join(d.page_content for d in found_docs)
#
#
# # Chat funksiyası (İpucundakı struktura uyğun)
# def chat(sual: str) -> str:
#     # 1. Uyğun sənədləri tapırıq
#     found_docs = retriever.invoke(sual)
#     context = format_docs(found_docs)
#
#     # 2. Tarixçəni yaddaşdan alırıq
#     history = memory.load_memory_variables({})["history"]
#
#     # 3. Zənciri (Chain) işə salırıq
#     chain = prompt | llm | StrOutputParser()
#     cavab = chain.invoke({
#         "context": context,
#         "history": history,
#         "question": sual
#     })
#
#     # 4. Söhbəti yaddaşa yazırıq
#     memory.save_context({"input": sual}, {"output": cavab})
#
#     return cavab
#
#
# # 5. TEST: 3 dövrlü söhbət
# print("--- Söhbət Başlayır ---")
#
# # 1-ci sual
# q1 = "Kursun müddəti nə qədərdir?"
# print(f"Sual: {q1}")
# print(f"Cavab: {chat(q1)}\n")
#
# # 2-ci sual
# q2 = "Qiyməti neçədir?"
# print(f"Sual: {q2}")
# print(f"Cavab: {chat(q2)}\n")
#
# # 3-cü sual (Əvvəlki cavaba istinad edir - Memory testi)
# q3 = "Bəs ödənişi necə edə bilərəm? Yuxarıda dediyin qiyməti hissəli ödəmək olar?"
# print(f"Sual: {q3}")
# print(f"Cavab: {chat(q3)}\n")