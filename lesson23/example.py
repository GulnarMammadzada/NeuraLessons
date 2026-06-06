from langchain_community import vectorstores
from langchain_text_splitters import CharacterTextSplitter

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

load_dotenv()
client = OpenAI()


#
# text="Baki seherinde hava cox gozeldir ve insanlar parkda gezmeyi sevir"
#
# text_splitter=CharacterTextSplitter(
#     separator=" ",
#     chunk_size=30,
#     chunk_overlap=15
# )
#
# chunks=text_splitter.split_text(text)
#
# for i,chunk in enumerate(chunks):
#     print(len(chunk),chunk)
#     print("---"*5)

#
# def get_embedding(text : str)->list[float]:
#     response=client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding
#
# def check_similarity(vector1,vector2):
#
#     a=np.array(vector1)
#     b=np.array(vector2)
#
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#
#
# text1="Men proqlasdirma oyrenirem ve python bilirem"
# text2="Men pyhton bilirem ve java oyrenirem"
# text3="Men biznes sahesinde calisiram"
#
# v1=get_embedding(text1)
# v2=get_embedding(text2)
# v3=get_embedding(text3)
#
# s1=check_similarity(v1,v2)
# s2=check_similarity(v1,v3)
# s3=check_similarity(v2,v3)
#
# print(s1)
# print(s2)
# print(s3)
#


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





# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document
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
#
# vectorstore=Chroma.from_documents(
#     documents=documents,
#     embedding=embeddings,
#     persist_directory="./my_chroma_db"
# )
#
# results=vectorstore.similarity_search(
#     query="Mehsulu nece qaytarmaq olar?",
#     k=2
# )
#
# for doc in results:
#     print(doc.page_content)
#     print(doc.metadata['source'])
#





# Bütün söhbəti saxlayır
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
#
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