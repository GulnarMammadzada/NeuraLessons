# #1
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # Faktoloji və ciddi cavablar üçün temperature = 0.0 təyin edirik
# support_model = ChatOpenAI(model="gpt-4o", temperature=0.0)
#
# # Şablonun qurulması
# support_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən 'TexnoAz' mağazasının müştəri xidmətləri təmsilçisisən. Müştərinin problemini dinlə və ona çox nəzakətli, həll yönümlü bir cavab yaz. Cavabın rəsmi və qısa olsun."),
#     ("human", "Məhsul: {məhsul}\nŞikayət: {şikayət}")
# ])
#
# # Parser
# parser = StrOutputParser()
#
# # Zəncirin qurulması (LCEL)
# support_chain = support_template | support_model | parser
#
# # Test edilməsi (Invoke)
# customer_complaint = {
#     "məhsul": "Ağıllı Saat (Smartwatch X)",
#     "şikayət": "Dünən aldım, amma batareyası cəmi 2 saat saxlayır və çox qızır."
# }
#
# response = support_chain.invoke(customer_complaint)
#
# print("--- TAPŞIRIQ 1: MÜŞTƏRİ XİDMƏTLƏRİ CAVABI ---")
# print(response)
#
#
# #2
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # Analitik izahlar üçün orta səviyyəli temperatur (0.3) idealdır
# sql_model = ChatOpenAI(model="gpt-4o", temperature=0.3)
#
# # Şablonun qurulması
# sql_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən təcrübəli bir Data Base Administratorusan (DBA). Sənə verilən SQL sorğusunu texniki olmayan bir insanın (məsələn, menecerin) başqa düşəcəyi şəkildə, addım-addım Azərbaycan dilində izah et."),
#     ("human", "Bu SQL sorğusunu izah et:\n{sql_query}")
# ])
#
# parser = StrOutputParser()
#
# # LCEL Pipeline
# sql_explainer_chain = sql_template | sql_model | parser
#
# # Test edilməsi
# complex_sql = """
# SELECT u.name, COUNT(o.id) as total_orders
# FROM users u
# JOIN orders o ON u.id = o.user_id
# WHERE o.order_date >= '2026-01-01'
# GROUP BY u.name
# HAVING COUNT(o.id) > 5;
# """
#
# response = sql_explainer_chain.invoke({"sql_query": complex_sql})
#
# print("--- TAPŞIRIQ 2: SQL İZAHI ---")
# print(response)
#
#
# #3
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # Yaradıcı kontent üçün yüksək temperatur (0.8) seçirik
# creative_model = ChatOpenAI(model="gpt-4o", temperature=0.8)
#
# # Şablonun qurulması
# instagram_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən trendləri izləyən rəqəmsal marketinq mütəxəssisisən. Verilən mövzuya uyğun, oxucunun diqqətini çəkən, emojilərlə zəngin bir Instagram postu yaz. Sonda mövzuya uyğun 5 hashtag əlavə et."),
#     ("human", "Mövzu: {mövzu}\nHədəf Kütlə: {hedef_kutle}")
# ])
#
# parser = StrOutputParser()
#
# # LCEL Pipeline
# insta_chain = instagram_template | creative_model | parser
#
# # Test edilməsi
# post_data = {
#     "mövzu": "Süni intellektin gündəlik həyatımızı asanlaşdıran 3 gizli funksiyası",
#     "hedef_kutle": "Gənc sahibkarlar və tələbələr"
# }
#
# post_data2 = {
#     "mövzu": "Süni intellektin gündəlik həyatımızı asanlaşdıran 3 gizli funksiyası",
#     "hedef_kutle": "Gənc sahibkarlar və tələbələr"
# }
# response = insta_chain.invoke(post_data)
# response2 = insta_chain.invoke(post_data2)
#
# print("--- TAPŞIRIQ 3: INSTAGRAM POSTU ---")
# print(response)
#
#
# #4
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # Klassifikasiya tapşırıqlarında dəqiqlik üçün temperature mütləq 0.0 olmalıdır
# tagger_model = ChatOpenAI(model="gpt-4o", temperature=0.0)
#
# # Şablonu elə qururuq ki, model qaydalardan kənara çıxmasın
# tagger_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən e-ticarət şərhlərini analiz edən süni intellektsən. İstifadəçi rəyini oxu və YALNIZ bu üç sözdən birini qaytar: 'POZİTİV', 'NEQATİV' və ya 'NEYTRAL'. Əlavə heç bir söz, nöqtə və ya izah yazma."),
#     ("human", "{rey}")
# ])
#
# parser = StrOutputParser()
# tagger_chain = tagger_template | tagger_model | parser
#
# # Test 1: Neqativ ssenari
# review_1 = "Məhsul sifarişdən 5 gün sonra gəldi və qutusu cırılmışdı. Heç bəyənmədim."
# result_1 = tagger_chain.invoke({"rey": review_1})
# print(f"Rəy 1 Nəticəsi: {result_1}")  # Çıxış: NEQATİV
#
# # Test 2: Pozitiv ssenari
# review_2 = "Çox keyfiyyətli materialı var, tam ölçümə uyğun gəldi. Təşəkkürlər!"
# result_2 = tagger_chain.invoke({"rey": review_2})
# print(f"Rəy 2 Nəticəsi: {result_2}")  # Çıxış: POZİTİV
#
#
#
# #5
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# localization_model = ChatOpenAI(model="gpt-4o", temperature=0.4)
#
# # Şablonda 3 fərqli dinamik dəyişən istifadə edirik
# loc_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən qlobal brendlərin lokalizasiya mütəxəssisisən. Sənə verilən mətni {hədəf_dil} dilinə tərcümə et. Tərcümə edərkən mətni {ölkə} mədəniyyətinə uyğunlaşdır və {ton} tondan istifadə et."),
#     ("human", "Mətn: {metn}")
# ])
#
# parser = StrOutputParser()
# localization_chain = loc_template | localization_model | parser
#
# # Test Data
# global_announcement = "Hey team! We are thrilled to announce that our platform just crossed 1 million users. Hard work pays off!"
#
# config = {
#     "hədəf_dil": "Azərbaycan dili",
#     "ölkə": "Azərbaycan",
#     "ton": "peşəkar və korporativ",
#     "metn": global_announcement
# }
#
# adapted_text = localization_chain.invoke(config)
# print("--- TAPŞIRIQ 6: LOKALİZASİYA NƏTİCƏSİ ---")
# print(adapted_text)
#
#
# #6
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
#
# load_dotenv()
#
# hr_model = ChatOpenAI(model="gpt-4o", temperature=0.6)
#
# hr_template = ChatPromptTemplate.from_messages([
#     ("system", "Sən təcrübəli Texniki HR (İnsan Resursları) mütəxəssisisən. Sənə təqdim olunan CV-ni analiz et. "
#                "Nəticədə namizədin 3 əsas güclü tərəfini qeyd et və müsahibədə ona verilməli olan 3 unikal texniki sual hazırla."),
#     ("human", "Vakansiya: {vakansiya}\nCV Mətni: {cv_metni}")
# ])
#
# parser = StrOutputParser()
# hr_chain = hr_template | hr_model | parser
#
# # Test Data
# cv_data = {
#     "vakansiya": "Senior Python Developer",
#     "cv_metni": "Ad: Elvin Məmmədov. Təcrübə: 5 il Django və FastApi ilə backend proqramlaşdırma. PostgreSQL və Redis verilənlər bazaları ilə işləmişəm. AWS mühitində tətbiqlərin yerləşdirilməsi (deployment) təcrübəm var. Komandada çevik (Agile) metodologiya ilə işləməyə vərdiş etmişəm."
# }
#
# hr_analysis = hr_chain.invoke(cv_data)
# print("--- TAPŞIRIQ 7: HR ANALİZİ VƏ SUALLAR ---")
# print(hr_analysis)


#7
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Qiymətləndirmədə ədalətli və sabit olmaq üçün aşağı temperatur
teacher_model = ChatOpenAI(model="gpt-4o", temperature=0.1)

teacher_template = ChatPromptTemplate.from_messages([
    ("system", "Sən ədalətli bir müəllimsən. Sənə verilən sualı, düzgün cavabı və tələbənin cavabını müqayisə et. "
               "Tələbəyə {maksimal_bal} üzərindən layiq olduğu balı ver. Əgər bal kəsirsənsə, səbəbini və doğrusunu izah et."),
    ("human", "Sual: {sual}\nDüzgün Cavab: {duzgun_cavab}\nTələbənin Cavabı: {telebenin_cavab}")
])

parser = StrOutputParser()
teacher_chain = teacher_template | teacher_model | parser

# Test Data (Tələbə qismən düzgün cavab verib)


grade_result = teacher_chain.invoke({"sual": "LangChain-də LCEL nədir və nə üçün istifadə olunur?",
    "duzgun_cavab": "LCEL (LangChain Expression Language) fərqli komponentləri pipe (|) operatoru ilə bir-birinə bağlamaq və deklarativ zəncirlər qurmaq üçün istifadə olunan sintaksisdir.",
    "telebenin_cavab": "LCEL zəncirlər qurmaq üçün bir dildir, komponentləri birləşdirir amma daxili işləmə prinsipini tam bilmirəm.",
    "maksimal_bal": "10"})

print("--- TAPŞIRIQ 8: MÜƏLLİM QİYMƏTLƏNDİRMƏSİ ---")
print(grade_result)