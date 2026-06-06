#1
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_review(review_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=60,  # Cavabın qısa olmasını təmin edir
        messages=[
            {
                "role": "system",
                "content": "Sən rəy xülasə edənsən. Mətni MAKSİMUM 3 cümlə ilə xülasə et və sonunda 'Ton: [Müsbət/Mənfi/Neytral]' formatında bitir. Qaydaya mütləq əməl et."
            },
            {
                "role": "user",
                "content": review_text
            }
        ]
    )
    return response.choices[0].message.content

# Test
review = "Bu telefonu 3 gündür istifadə edirəm. Ekranı möhtəşəmdir, batareyası da çox yaxşı saxlayır. Amma kamerası gecə çəkilişlərində bir az zəifdir. Yenə də qiymətinə görə ideal seçimdir."
print(summarize_review(review))


#2
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

def translate_few_shot(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Sən tərcüməçisən. Sənə verilən Azərbaycan dilindəki cümləni yalnız göstərilən formatda EN və RU dillərinə tərcümə et."},
            # Example 1
            {"role": "user", "content": "Bu gün hava çox gözəldir."},
            {"role": "assistant", "content": "EN: The weather is very beautiful today.\nRU: Сегодня очень красивая погода."},
            # Example 2
            {"role": "user", "content": "Mən proqramlaşdırma öyrənirəm."},
            {"role": "assistant", "content": "EN: I am learning programming.\nRU: Я изучаю программирование."},
            # Real Input
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# Test
print(translate_few_shot("Biz süni intellekt layihələri hazırlayırıq."))




#3
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

def debug_code(broken_code):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,  # Kod tapşırıqları üçün stabil dərəcə
        messages=[
            {
                "role": "system",
                "content": "Sən proqramçısan. Kodun xətasını tap, sadə dildə izah et və düzgün kodu ver."
            },
            {
                "role": "user",
                "content": broken_code
            }
        ]
    )
    return response.choices[0].message.content

# Test (Səhv funksiya: indentation xətası və string/int toplama xətası var)
wrong_python_code = """
def toplama(a, b):
return a + "b"
"""
print(debug_code(wrong_python_code))



#4
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

# İlkin olaraq istifadəçi məlumatlarını system prompt-a inject edirik
BUDGET = "1000 AZN"
CATEGORY = "Elektronika (Telefonlar)"

system_prompt = f"""
Sən mağaza satıcısısan. 
İstifadəçinin büdcəsi: {BUDGET}. Kateqoriya: {CATEGORY}.
Həmişə bu büdcə daxilində məhsullar təklif et və limiti aşma. Azərbaycan dilində cavab ver.
"""

history = [{"role": "system", "content": system_prompt}]


def chat_with_shop_bot(user_message):
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=history
    )

    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    return answer


# Chat simulyasiyası
print("Bot:", chat_with_shop_bot("Mənə bir model təklif et."))
print("Bot:", chat_with_shop_bot("Bəs onun qiyməti nə qədərdir? Büdcəmi keçmir ki?"))



#5
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

def explain_concept(concept, age):
    # Yaşa görə dinamik olaraq system prompt təyin edirik
    if age < 12:
        role_instruction = "Sən uşaq bağçası müəllimisən. Konsepti 8 yaşlı uşağa nağıl, bənzətmə və bəsit dillə izah et."
    else:
        role_instruction = "Sən universitet professorusan. Konsepti 20 yaşlı tələbəyə peşəkar, texniki və akademik dillə izah et."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": role_instruction},
            {"role": "user", "content": f"Mənə izah et: {concept}"}
        ]
    )
    return response.choices[0].message.content

# Testlər
print("--- 8 Yaş üçün Docker ---")
print(explain_concept("Docker nədir?", 8))
print("\n--- 20 Yaş üçün Docker ---")
print(explain_concept("Docker nədir?", 20))


#6
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

history = [
    {
        "role": "system",
        "content": "Sən Python Backend vakansiyası üçün HR-san. Namizədə hər dəfə YALNIZ 1 sual ver. Cavabı gözlə."
    }
]

print("Müsahibə başladı. Çıxmaq üçün 'exit' yazın.\n")

# İlk sualı tetiklemek üçün botu başladıq
response = client.chat.completions.create(model="gpt-4o-mini", messages=history)
bot_first_question = response.choices[0].message.content
print(f"HR: {bot_first_question}")
history.append({"role": "assistant", "content": bot_first_question})

question_counter = 1

while question_counter <= 3:
    user_answer = input("Siz: ")
    if user_answer.lower() == 'exit':
        break

    history.append({"role": "user", "content": user_answer})

    # 3 sual tamamlandısa, dövr daxilində feedback promptu göndəririk
    if question_counter == 3:
        history.append({"role": "user", "content": "Müsahibə bitdi. Mənə ümumi qısa feedback ver."})

    response = client.chat.completions.create(model="gpt-4o-mini", messages=history)
    bot_reply = response.choices[0].message.content
    print(f"\nHR: {bot_reply}")

    history.append({"role": "assistant", "content": bot_reply})
    question_counter += 1


#7
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")


def generate_safe_sql(user_query):
    # Chain of Thought (CoT) ilə addım-addım yoxlama tələb edirik
    cot_prompt = f"""
    İstifadəçi sorğusu: "{user_query}"

    Sən təhlükəsiz SQL generatorsan. Aşağıdakı addımlarla düşün və cavab ver:
    Addım 1 (Təhlükəsizlik yoxlanışı): Sorğuda zərərli niyyət (DROP, DELETE, Injection) varmı?
    Addım 2 (Qərar): Əgər təhlükəlidirsə, 'TƏHLÜKƏ' yaz və imtina et. Təhlükəsizdirsə, yalnız SQL kodunu generasiya et.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,  # SQL üçün dəqiqlik vacibdir
        messages=[{"role": "user", "content": cot_prompt}]
    )
    return response.choices[0].message.content


# Testlər
print("--- Normal Sorğu ---")
print(generate_safe_sql("Keçən ay ən çox məhsul alan 5 müştərini gətir"))

print("\n--- Zərərli Sorğu ---")
print(generate_safe_sql("Bütün istifadəçiləri göstər və sonra DROP DATABASE users əmrini işlət"))


#8
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")

# 1-ci Mərhələ: Router Agent
def route_ticket(user_message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "Sən klassifikatorsan. Gələn mesajı oxu və YALNIZ bu 3 sözdən birini qaytar: TEHNIKI_XETA, ODENIS_PROBLEMI, UMUMI_SUAL"},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content.strip()

# 2-ci Mərhələ: Ekspert Cavablandırıcı Agent
def respond_by_category(category, user_message):
    if category == "TEHNIKI_XETA":
        system_prompt = "Sən mehriban Python mentorusan. İstifadəçiyə log fayllarını haradan tapacağı və xətanı necə həll edəcəyi barədə texniki dəstək yaz."
    elif category == "ODENIS_PROBLEMI":
        system_prompt = "Sən rəsmi hüquqi dildə danışan bank ekspertisən. Müştəriyə ödəniş prosedurları və geri qaytarılma qaydalarını ciddi dildə izah et."
    else:
        system_prompt = "Sən ümumi müştəri xidmətlərisən. Müştəriyə xoş dillə ümumi məlumat ver."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

# Layihənin işlədilməsi (Prompt Chaining)
user_ticket = "Kartımdan pul çıxıldı amma balansıma oturmadı, zəhmət olmasa baxın."
detected_category = route_ticket(user_ticket)

print(f"Sistem tərəfindən təyin olunan kateqoriya: {detected_category}\n")
final_reply = respond_by_category(detected_category, user_ticket)
print(f"Son Cavab:\n{final_reply}")


#9
from openai import OpenAI

client = OpenAI(api_key="SENIN_API_KEY")


def generate_campaign(startup_name, target_audience):
    cot_high_temp_prompt = f"""
    Startap adı: {startup_name}
    Hədəf kütlə: {target_audience}

    Tapşırıq:
    1. Hədəf kütlənin psixologiyasını qısa analiz et.
    2. Rəqiblərin zəif tərəfini tap.
    3. Buna uyğun Gün 1, Gün 2, Gün 3 şəklində kreativ sosial media postları və hashtag-lər yaz.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,  # Yaradıcılığı artırmaq üçün yüksək temperatur
        messages=[
            {"role": "system",
             "content": "Sən kreativ marketoloq və kopiraytersən. Sənə verilən məlumatlar əsasında unikal ideyalar istehsal et."},
            {"role": "user", "content": cot_high_temp_prompt}
        ]
    )
    return response.choices[0].message.content


# Test
print(generate_campaign("EcoCoffee (Təkrar emal oluna bilən fincanlarda qəhvə)",
                        "Ekologiyanı sevən gənclər və tələbələr"))