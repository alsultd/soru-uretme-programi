from docx import Document
import random
from transformers import pipeline

def get_topic_text(doc_path, topic_no):
    doc = Document(doc_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    topics = []
    current_topic = ""
    current_number = None

    for p in paragraphs:
        if p.startswith("Konu:"):
            if current_topic and current_number is not None:
                topics.append((current_number, current_topic.strip()))
            current_number = int(p.replace("Konu:", "").strip())
            current_topic = ""
        else:
            current_topic += p + "\n"

    if current_topic and current_number is not None:
        topics.append((current_number, current_topic.strip()))

    for number, text in topics:
        if number == topic_no:
            return text
    return None

def main():
    doc_path = r"C:\Users\PC\OneDrive\Masaüstü\soru-uretme-programi\OCR_Ana_Cikti_Guncel.docx"

    try:
        topic_no = int(input("Konu numarasını girin (1-150): "))
    except ValueError:
        print("Geçersiz sayı!")
        return

    topic_text = get_topic_text(doc_path, topic_no)

    if topic_text is None:
        print("Konu bulunamadı.")
        return

    print("\n=== Okuma Parçası ===\n")
    print(topic_text)

    print("\n=== Sorular Üretiliyor ===\n")
    question_generator = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-question-generation-ap")

    questions = question_generator(topic_text, max_length=64, num_return_sequences=3)

    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['generated_text']}")

if __name__ == "__main__":
    main()

