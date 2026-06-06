from openai import OpenAI
import json
import tiktoken
from datetime import datetime

client = OpenAI(
    api_key="Your_Api_Key"
)

# ============================================================
# TASK 01 — Şəxsiyyətə uyğun tövsiyəçi
# System prompt · Few-shot · Temperature müqayisəsi
# ============================================================
def task01():
    print("\n" + "="*60)
    print("TASK 01 — Şəxsiyyətə uyğun tövsiyəçi")
    print("="*60)

    hobsi   = input("Hobbin nədir? ")
    pese    = input("Peşən nədir? ")
    maraq   = input("Maraq sahən nədir? ")

    system_prompt = f"""
Sən şəxsiyyətə uyğun tövsiyə verən bir köməkçisən.
İstifadəçi haqqında məlumat:
- Peşəsi: {pese}
- Hobbisi: {hobsi}
- Maraq sahəsi: {maraq}
Bu məlumatları nəzərə alaraq tövsiyə ver.
Azərbaycan dilində cavab ver.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": """
Rəy: Mən mühasibəm, kitab oxumağı sevirəm, maliyyə maraqlanıram.
Tövsiyə: 1) "Rich Dad Poor Dad" kitabı 2) Coursera maliyyə kursu 3) "The Big Short" filmi
"""
        },
        {
            "role": "user",
            "content": """
Rəy: Mən dizaynerəm, rəsm çəkirəm, incəsənət maraqlanıram.
Tövsiyə: 1) "The Shape of Design" kitabı 2) Skillshare illüstrasiya kursu 3) "The Great Beauty" filmi
"""
        },
        {
            "role": "user",
            "content": "Mənə 3 tövsiyə ver: 1 kitab, 1 kurs, 1 film."
        }
    ]

    print("\n--- Temperature = 0.2 (stabil) ---")
    cavab_02 = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=messages
    )
    print(cavab_02.choices[0].message.content)

    print("\n--- Temperature = 0.8 (yaradıcı) ---")
    cavab_08 = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        messages=messages
    )
    print(cavab_08.choices[0].message.content)

    print("\n--- Fərq ---")
    print("Temperature=0.2 daha stabil və gözlənilən tövsiyələr verir.")
    print("Temperature=0.8 daha yaradıcı və gözlənilməz seçimlər edir.")


# ============================================================
# TASK 02 — System prompt ilə rol vermək
# System prompt · Müqayisə
# ============================================================
def task02():
    print("\n" + "="*60)
    print("TASK 02 — System prompt ilə rol vermək")
    print("="*60)

    sual = "Fotosintez nədir?"

    print("\n--- System prompt İLƏ (uşaq müəllimi) ---")
    cavab_muellim = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
Sən uşaqlara dərs deyən müəllimsən.
Qaydalar:
- Çox sadə dildə danış, 8-10 yaşlı uşaq anlasın
- Gündəlik həyatdan nümunə ver
- Qısa və aydın izah et
- Azərbaycan dilində cavab ver
"""
            },
            {"role": "user", "content": sual}
        ]
    )
    print(cavab_muellim.choices[0].message.content)

    print("\n--- System prompt OLMADAN ---")
    cavab_normal = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": sual}
        ]
    )
    print(cavab_normal.choices[0].message.content)

    print("\n--- Müqayisə ---")
    print("Müəllim rolu: sadə dil, gündəlik nümunə, qısa izah.")
    print("Normal cavab: texniki dil, daha ətraflı, rəsmi üslub.")


# ============================================================
# TASK 03 — Few-shot sentiment analizi
# Few-shot · Çoxlu request
# ============================================================
def task03():
    print("\n" + "="*60)
    print("TASK 03 — Few-shot sentiment analizi")
    print("="*60)

    test_reyleri = [
        "Məhsul gözləntilərimə tam cavab verdi, çox məmnunam!",
        "Çatdırılma çox gecikdi, bir daha sifariş etməyəcəm.",
        "Normal idi, nə yaxşı nə pis.",
        "Keyfiyyət əla, qiymət də münasibdir, tövsiyə edirəm!",
        "Paket zədələnmiş gəldi, içindəki məhsul da sınmışdı."
    ]

    few_shot_messages = [
        {"role": "system", "content": "Sən sentiment analizi aparırsın. Yalnız 'Müsbət', 'Mənfi' və ya 'Neytral' cavab ver."},
        {"role": "user",      "content": "Rəy: Məhsul çox yaxşıdır, hər şey mükəmməl idi."},
        {"role": "assistant", "content": "Müsbət"},
        {"role": "user",      "content": "Rəy: Keyfiyyət tamamilə pisdir, pulum boşa getdi."},
        {"role": "assistant", "content": "Mənfi"},
        {"role": "user",      "content": "Rəy: Nə yaxşı nə də pis, sadəcə adi bir məhsul."},
        {"role": "assistant", "content": "Neytral"},
    ]

    print(f"\n{'Rəy':<55} {'Sentiment'}")
    print("-" * 70)

    for rey in test_reyleri:
        messages = few_shot_messages + [
            {"role": "user", "content": f"Rəy: {rey}"}
        ]
        cavab = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.0,
            messages=messages
        )
        sentiment = cavab.choices[0].message.content.strip()
        print(f"{rey[:52]:<55} {sentiment}")


# ============================================================
# TASK 04 — Yaddaşlı chatbot
# History · While loop
# ============================================================
def task04():
    print("\n" + "="*60)
    print("TASK 04 — Yaddaşlı chatbot")
    print("="*60)
    print("Chatbot başladı. Çıxmaq üçün 'exit' yaz.\n")

    history = [
        {
            "role": "system",
            "content": """
Sən mehriban bir köməkçisən.
İstifadəçinin adını, şəhərini və söhbət boyunca dediklərini xatırla.
Azərbaycan dilində cavab ver.
"""
        }
    ]

    while True:
        user_input = input("Sən: ").strip()
        if user_input.lower() == "exit":
            print("Chatbot: Görüşənədək!")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        cavab = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.5,
            messages=history
        )

        bot_cavabi = cavab.choices[0].message.content
        history.append({"role": "assistant", "content": bot_cavabi})
        print(f"Bot: {bot_cavabi}\n")


# ============================================================
# TASK 05 — AI Şair
# Temperature kontrast · CoT qiymətləndirmə
# ============================================================
def task05():
    print("\n" + "="*60)
    print("TASK 05 — AI Şair")
    print("="*60)

    sozler = input("3 söz yaz (vergüllə ayır): ")

    system_prompt = """
Sən peşəkar Azərbaycan şairisən.
Verilən sözləri mütləq istifadə edərək şeir yaz.
Şeir 4 bənddən ibarət olsun.
Yalnız Azərbaycan dilində yaz.
"""

    prompt = f"Bu 3 sözü istifadə edərək şeir yaz: {sozler}"

    print("\n--- Temperature = 0.2 (klassik, stabil) ---")
    sair_02 = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt}
        ]
    )
    seir_1 = sair_02.choices[0].message.content
    print(seir_1)

    print("\n--- Temperature = 0.9 (yaradıcı, eksperimental) ---")
    sair_09 = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.9,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt}
        ]
    )
    seir_2 = sair_09.choices[0].message.content
    print(seir_2)

    print("\n--- CoT Qiymətləndirmə ---")
    qiymetlendirme = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "Sən ədəbi tənqidçisən. Şeirləri obyektiv qiymətləndir."
            },
            {
                "role": "user",
                "content": f"""
İki şeiri müqayisə et və hansının daha güclü olduğunu müəyyən et.

Şeir 1 (stabil):
{seir_1}

Şeir 2 (yaradıcı):
{seir_2}

Addım 1: Hər şeirin güclü tərəflərini tap.
Addım 2: Hər şeirin zəif tərəflərini tap.
Addım 3: Qalibi elan et və niyə olduğunu izah et.
"""
            }
        ]
    )
    print(qiymetlendirme.choices[0].message.content)


# ============================================================
# TASK 06 — Tarix müəllimi chatbotu
# History · Test sualı · Xülasə
# ============================================================
def task06():
    print("\n" + "="*60)
    print("TASK 06 — Tarix müəllimi chatbotu")
    print("="*60)
    print("Tarix mövzusu yaz. 5 mövzudan sonra xülasə göstəriləcək.")
    print("Çıxmaq üçün 'exit' yaz.\n")

    history = [
        {
            "role": "system",
            "content": """
Sən tarix müəllimsən.
Qaydalar:
- İstifadəçi mövzu yazanda əvvəlcə qısa izah ver
- İzahın sonuna mütləq 1 test sualı əlavə et
- İstifadəçi cavab verəndə düzgün/yanlış de və izah et
- Azərbaycan dilində danış
- Hər cavabın sonuna "[Test sualı: ...]" formatında sual yaz
"""
        }
    ]

    movzu_sayi = 0
    dogru_sayi = 0

    while True:
        user_input = input("Sən: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        cavab = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.4,
            messages=history
        )

        bot_cavabi = cavab.choices[0].message.content
        history.append({"role": "assistant", "content": bot_cavabi})
        print(f"\nMüəllim: {bot_cavabi}\n")

        if "[Test sualı:" in bot_cavabi:
            movzu_sayi += 1

            if movzu_sayi == 5:
                print("\n--- 5 Mövzu Tamamlandı — Xülasə ---")
                xulase = client.chat.completions.create(
                    model="gpt-4o",
                    temperature=0.3,
                    messages=history + [
                        {
                            "role": "user",
                            "content": "Söhbəti xülasə et: neçə sual verildi, istifadəçi hansı mövzularda güclü, hansılarda zəif idi? Tövsiyə ver."
                        }
                    ]
                )
                print(xulase.choices[0].message.content)
                break


# ============================================================
# TASK 07 — Mübahisə məşqçisi
# Dinamik system prompt · CoT · Temperature
# ============================================================
def task07():
    print("\n" + "="*60)
    print("TASK 07 — Mübahisə məşqçisi")
    print("="*60)

    movzu = input("Mübahisə mövzusu yaz (məs: 'Universitet məcburidirmi?'): ")

    print("\n--- Hər iki tərəfin arqumentləri ---")
    arqumentler = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "Sən mübahisə analitikisən. Azərbaycan dilində cavab ver."
            },
            {
                "role": "user",
                "content": f"""
Mövzu: {movzu}
Lehinə 3 güclü arqument ver.
Əleyhinə 3 güclü arqument ver.
Formatla:
LEHİNƏ:
1. ...
2. ...
3. ...
ƏLEYHİNƏ:
1. ...
2. ...
3. ...
"""
            }
        ]
    )
    print(arqumentler.choices[0].message.content)

    tercih = input("\nHansı tərəfi seçirsən? (lehinə/əleyhinə): ").strip().lower()
    eks_teref = "əleyhinə" if tercih == "lehinə" else "lehinə"

    print(f"\nBot indi '{eks_teref}' tərəfindədir. Mübahisə başlayır!")
    print("4 tur sonra qalıb müəyyən ediləcək. 'bitir' yaz — erkən bitirmək üçün.\n")

    history = [
        {
            "role": "system",
            "content": f"""
Sən mübahisəçisən. Mövzu: {movzu}
Sən {eks_teref} tərəfindəsən.
İstifadəçinin hər arqumentini çürüt.
Qısa, güclü, məntiqli cavab ver.
Azərbaycan dilində danış.
"""
        }
    ]

    for tur in range(1, 5):
        print(f"--- Tur {tur} ---")
        user_arg = input("Sənin arqumentin: ").strip()
        if user_arg.lower() == "bitir":
            break

        history.append({"role": "user", "content": user_arg})

        cavab = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.6,
            messages=history
        )
        bot_cavabi = cavab.choices[0].message.content
        history.append({"role": "assistant", "content": bot_cavabi})
        print(f"Bot: {bot_cavabi}\n")

    print("\n--- CoT Qiymətləndirmə ---")
    qiymet = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=history + [
            {
                "role": "user",
                "content": """
Mübahisəni qiymətləndir:
Addım 1: İstifadəçinin arqumentlərini analiz et.
Addım 2: Botun arqumentlərini analiz et.
Addım 3: Hansı tərəf daha güclü dəlil gətirdi? Qalibi elan et.
"""
            }
        ]
    )
    print(qiymet.choices[0].message.content)


# ============================================================
# TASK 08 — Hekayə yazıçısı botu
# Few-shot · History · CoT final · Temperature
# ============================================================
def task08():
    print("\n" + "="*60)
    print("TASK 08 — Hekayə yazıçısı botu")
    print("="*60)
    print("'davam et' — hekayəni uzat | 'son' — final yaz\n")

    janr    = input("Janr (məs: fantastika, dram, gərginlik): ")
    qehreman = input("Qəhrəman adı: ")
    problem = input("Əsas problem: ")

    few_shot = """
Nümunə:
Janr: macəra | Qəhrəman: Leyla | Problem: xəritə itib
Hekayə əvvəli:
Leyla meşənin ortasında dayanmışdı. Əlindəki xəritə bir an əvvəl küləyin qoynunda uçub getmişdi.
Ətrafda heç nə tanış deyildi — nə dağ, nə çay, nə də bir iz.
Axşam düşürdü. Və meşənin dərinliyindən qəribə bir səs gəlirdi...
"""

    history = [
        {
            "role": "system",
            "content": f"""
Sən yaradıcı hekayə yazıçısısan.
Janr: {janr}
Qəhrəman: {qehreman}
Problem: {problem}
Hər dəfə 3-4 cümlə yaz, gərginliyi artır.
Azərbaycan dilində yaz.
"""
        },
        {
            "role": "user",
            "content": f"{few_shot}\nİndi mənim hekayəmi başlat: Janr: {janr} | Qəhrəman: {qehreman} | Problem: {problem}"
        }
    ]

    print("\n--- Hekayə başlayır ---\n")
    baslangic = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        messages=history
    )
    metn = baslangic.choices[0].message.content
    history.append({"role": "assistant", "content": metn})
    tam_hekaye = metn
    print(metn)

    while True:
        emr = input("\n[davam et / son]: ").strip().lower()

        if emr == "son":
            print("\n--- Final ---\n")
            history.append({
                "role": "user",
                "content": """
Addım 1: Əsas konflikti xatırla.
Addım 2: Bütün ipuclarını birləşdir.
Addım 3: Güclü, gözlənilməz final yaz — son cümlə yadda qalmalıdır.
"""
            })
            final = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.7,
                messages=history
            )
            final_metn = final.choices[0].message.content
            tam_hekaye += "\n\n" + final_metn
            print(final_metn)

            print("\n" + "="*60)
            print("TAM HEKAYƏ")
            print("="*60)
            print(tam_hekaye)
            break

        elif emr == "davam et":
            history.append({"role": "user", "content": "Hekayəni davam etdir."})
            davam = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.8,
                messages=history
            )
            davam_metn = davam.choices[0].message.content
            history.append({"role": "assistant", "content": davam_metn})
            tam_hekaye += "\n\n" + davam_metn
            print(davam_metn)


# ============================================================
# TASK 09 — Adaptiv müsahib botu
# JSON · Few-shot · CoT · Token idarəsi · Hesabat
# ============================================================
def task09():
    print("\n" + "="*60)
    print("TASK 09 — Adaptiv müsahib botu")
    print("="*60)

    vezife = input("Hədəf vəzifəni yaz (məs: backend developer): ")

    system_content = f"""
Sən {vezife} vəzifəsi üçün müsahib aparıcısısan.
Hər cavabı əvvəlkilərə baxaraq qiymətləndir.
Azərbaycan dilində danış.
"""

    history = [{"role": "system", "content": system_content}]

    encoder = tiktoken.encoding_for_model("gpt-4o")

    def token_say(msgs):
        return sum(len(encoder.encode(m["content"])) for m in msgs)

    def compress_history(hist):
        system = hist[0]
        danisiq = hist[1:]
        if len(danisiq) < 4:
            return hist
        xulase_ucun = danisiq[:-2]
        saxla = danisiq[-2:]
        xulase_metn = " | ".join(
            m["content"][:80] for m in xulase_ucun
        )
        return [system, {"role": "assistant", "content": f"[Xülasə: {xulase_metn}]"}] + saxla

    print("\n--- 5 Müsahibə sualı hazırlanır ---")
    few_shot_misal = """
Misal:
Sual: REST API ilə GraphQL arasındakı fərq nədir?
Cavab: REST hər endpoint üçün ayrı URL istifadə edir...
Qiymət: 7/10 — texniki anlama var, amma praktik nümunə çatışmadı.
"""

    sual_req = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=history + [
            {
                "role": "user",
                "content": f"""
{few_shot_misal}
{vezife} vəzifəsi üçün 5 müsahibə sualı hazırla.
Yalnız JSON formatında cavab ver, başqa heç nə yazma:
{{"suallar": ["sual1", "sual2", "sual3", "sual4", "sual5"]}}
"""
            }
        ]
    )

    raw = sual_req.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    suallar = json.loads(raw)["suallar"]

    print("Suallar hazırdır!\n")

    ballar = []

    for i, sual in enumerate(suallar, 1):
        print(f"\nSual {i}: {sual}")
        cavab = input("Cavabın: ").strip()

        history.append({"role": "user", "content": f"Sual: {sual}\nCavab: {cavab}"})

        if token_say(history) > 3000:
            print("[Token limiti keçildi — history sıxılır...]")
            history = compress_history(history)

        qiymet_req = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.2,
            messages=history + [
                {
                    "role": "user",
                    "content": f"""
Bu cavabı qiymətləndir:
Addım 1: Cavabın texniki dəqiqliyini yoxla.
Addım 2: Çatışmayan məqamları tap.
Addım 3: 0-10 bal ver və qısa rəy yaz.
Formatla: Bal: X/10 | Rəy: ...
"""
                }
            ]
        )

        qiymet_metn = qiymet_req.choices[0].message.content
        history.append({"role": "assistant", "content": qiymet_metn})
        print(f"Qiymət: {qiymet_metn}")

        try:
            bal = int(qiymet_metn.split("Bal:")[1].split("/")[0].strip())
            ballar.append(bal)
        except:
            ballar.append(5)

        print(f"[History: {token_say(history)} token]")

    print("\n" + "="*60)
    print("MÜSAHİBƏ HESABATI")
    print("="*60)

    hesabat = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=history + [
            {
                "role": "user",
                "content": f"""
Bütün müsahibəni qiymətləndir:
- Toplam bal: {sum(ballar)}/50
- Ortalama: {sum(ballar)/len(ballar):.1f}/10
Güclü tərəflərini, zəif tərəflərini və tövsiyəni yaz.
"""
            }
        ]
    )
    print(hesabat.choices[0].message.content)


# ============================================================
# TASK 10 — Şəxsi öyrənmə yol xəritəsi
# Pipeline · Gap analysis · CoT · Few-shot · Token sıxışdırma
# ============================================================
def task10():
    print("\n" + "="*60)
    print("TASK 10 — Şəxsi öyrənmə yol xəritəsi")
    print("="*60)

    ad         = input("Adın nədir? ")
    bacariqlar = input("Cari bacarıqların (vergüllə): ")
    hedef      = input("Hədəf vəzifən: ")

    system_content = f"""
Sən {ad} üçün şəxsi mentorsan.
Cari bacarıqlar: {bacariqlar}
Hədəf: {hedef}
Azərbaycan dilində danış. Həvəsləndirici ol.
"""

    history = [{"role": "system", "content": system_content}]
    encoder = tiktoken.encoding_for_model("gpt-4o")

    def token_say(msgs):
        return sum(len(encoder.encode(m["content"])) for m in msgs)

    def compress(hist):
        system = hist[0]
        qalan  = hist[1:]
        if len(qalan) < 6:
            return hist
        kohneler   = qalan[:-4]
        saxlananlar = qalan[-4:]
        xulase = " | ".join(m["content"][:60] for m in kohneler)
        return [system, {"role": "assistant", "content": f"[Əvvəlki progress xülasəsi: {xulase}]"}] + saxlananlar

    # Addım 1: Gap analysis
    print("\n--- Boşluq analizi aparılır ---")
    gap_req = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=history + [
            {
                "role": "user",
                "content": f"""
{hedef} vəzifəsi üçün boşluq analizi et.
Yalnız JSON formatında cavab ver:
{{"catismayanlar": ["bacariq1", "bacariq2"], "prioritet": ["en_vacib", "ikinci"]}}
"""
            }
        ]
    )
    raw = gap_req.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    gap = json.loads(raw)
    print(f"Çatışmayanlar: {', '.join(gap['catismayanlar'])}")
    print(f"Prioritet: {', '.join(gap['prioritet'])}")

    # Addım 2: Roadmap
    print("\n--- 4 həftəlik plan hazırlanır ---")

    few_shot_plan = """
Nümunə:
Həftə 1: {"movzu": "Python əsasları", "resurslar": ["Python.org dərslər", "CS50P kursu"], "hedef": "dəyişən, funksiya, loop öyrən"}
"""

    plan_req = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=history + [
            {
                "role": "user",
                "content": f"""
{few_shot_plan}
Addım 1: Çatışmayan bacarıqları prioritetə görə sırala.
Addım 2: Hər həftə üçün əsas mövzu müəyyən et.
Addım 3: 4 həftəlik plan JSON formatında yaz.
{{"plan": [{{"hefte": 1, "movzu": "...", "resurslar": [...], "hedef": "..."}}, ...]}}
"""
            }
        ]
    )
    raw2 = plan_req.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    plan = json.loads(raw2)["plan"]

    print("\n4 Həftəlik Plan:")
    for h in plan:
        print(f"\nHəftə {h['hefte']}: {h['movzu']}")
        print(f"  Resurslar: {', '.join(h['resurslar'])}")
        print(f"  Hədəf: {h['hedef']}")

    # Addım 3: Gündəlik progress
    print("\n--- Gündəlik progress izləmə başlayır ---")
    print("Hər gün nə öyrəndiyini yaz. 'hesabat' yaz — final hesabatı göstər.\n")

    gun = 1
    ballar = []

    while True:
        progress = input(f"Gün {gun} — Bu gün nə öyrəndin? ").strip()
        if progress.lower() == "hesabat":
            break

        history.append({"role": "user", "content": f"Gün {gun} progress: {progress}"})

        if token_say(history) > 3500:
            print("[Token limiti — history sıxılır...]")
            history = compress(history)

        qiymet = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.2,
            messages=history + [
                {
                    "role": "user",
                    "content": """
Bu günün progressini qiymətləndir:
Addım 1: Nə öyrənildi?
Addım 2: Plana uyğunmu?
Addım 3: Sabah üçün tövsiyə + bal ver (0-10).
Formatla: Bal: X/10 | ...
"""
                }
            ]
        )

        qiymet_metn = qiymet.choices[0].message.content
        history.append({"role": "assistant", "content": qiymet_metn})
        print(f"Mentor: {qiymet_metn}\n")
        print(f"[History: {token_say(history)} token]")

        try:
            bal = int(qiymet_metn.split("Bal:")[1].split("/")[0].strip())
            ballar.append(bal)
        except:
            ballar.append(5)

        gun += 1

    # Final hesabat
    print("\n" + "="*60)
    print("FİNAL HESABAT")
    print("="*60)

    ort = sum(ballar) / len(ballar) if ballar else 0

    final = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.5,
        messages=history + [
            {
                "role": "user",
                "content": f"""
{ad} üçün final hesabat yaz:
- Ümumi gün: {gun - 1}
- Ortalama bal: {ort:.1f}/10
- Güclü tərəflər, zəif tərəflər, növbəti addımlar
- Sonda {ad}-a həvəsləndirici motivasiya məktubu yaz
"""
            }
        ]
    )
    print(final.choices[0].message.content)


# ============================================================
# ANA MENYU
# ============================================================
def menu():
    tasklar = {
        "1":  ("Şəxsiyyətə uyğun tövsiyəçi",    task01),
        "2":  ("System prompt ilə rol vermək",    task02),
        "3":  ("Few-shot sentiment analizi",       task03),
        "4":  ("Yaddaşlı chatbot",                task04),
        "5":  ("AI şair",                         task05),
        "6":  ("Tarix müəllimi chatbotu",          task06),
        "7":  ("Mübahisə məşqçisi",               task07),
        "8":  ("Hekayə yazıçısı botu",            task08),
        "9":  ("Adaptiv müsahib botu",            task09),
        "10": ("Şəxsi öyrənmə yol xəritəsi",      task10),
    }

    while True:
        print("\n" + "="*60)
        print("LLM & PROMPT ENGINEERING — TASK SEÇİMİ")
        print("="*60)
        for n, (ad, _) in tasklar.items():
            print(f"  {n:>2}. {ad}")
        print("   0. Çıx")
        print("="*60)

        secim = input("Task nömrəsi seç: ").strip()
        if secim == "0":
            print("Görüşənədək!")
            break
        elif secim in tasklar:
            tasklar[secim][1]()
        else:
            print("Yanlış seçim. Yenidən cəhd et.")


if __name__ == "__main__":
    menu()