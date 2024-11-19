from transformers import pipeline
import re

# Загрузка модели
print("Loading model...")
pipe = pipeline("fill-mask", model="ai-forever/ruRoberta-large")
print("Model loaded.")

# Функция для поиска и замены сокращений
def find_and_replace_abbreviations(text):
    # Регулярное выражение для поиска любых сокращений, которые могут быть с точкой на конце или дефисом
    abbreviations = re.findall(r'\b\w{2,}\.|\w+-ие\b|\w{2,}-\w{2,}\b', text)  # добавляем возможность захватывать дефисы и сокращения
    print(f"Найденные сокращения: {abbreviations}")  # Для отладки

    results = []

    for abbr in abbreviations:
        masked_text = text.replace(abbr, "<mask>")  # Заменяем сокращение на <mask>
        predictions = pipe(masked_text)  # Получаем предсказания модели

        # Извлекаем слово с наибольшей вероятностью
        best_prediction = max(predictions, key=lambda x: x['score'])

        results.append({
            "original_text": text,
            "masked_text": masked_text,
            "abbreviation": abbr,
            "predicted_word": best_prediction['token_str'],
            "probability": best_prediction['score']
        })

    return results


# Тестовые примеры
test_cases = [
    "Мама мыла р.",  # Простой случай
    "Учитель дал задание прочитать произведение сор.",  # Сокращение сор.
    "Сегодня у нас лекция на тему 'Развитие делив.'",  # Сокращение делив.
    "На уроке химии мы изучали сокр. кислорода.",  # Сокращение сокр.
    "Работа аспиранта по теме 'сокр.' была отправлена на проверку.",  # Академический контекст
    "Сегодня на собрании обсуждали новую стратегию компании и её влияние на сокр.",  # Бизнес-контекст
    "Докладчик из министерства говорил об улучшении условий сокр.",  # Официальная речь
    "На уроке физкультуры преподаватель дал задание сделать 10 подходов к сокр.",  # Спортивный контекст
    "В процессе производства важно следить за качеством продукции и сокр.",  # Производственный контекст
    "Произведение Дарвина о сокр. стало предметом обсуждения.",  # Исторический контекст
    "Скоро приедет проф. консультант по вопросам экологии.",  # Сокращение проф.
    "Экономика и финансы изучаются на лекции в ВШЭ по теме 'бюдж.'",  # Сокращение бюджета
    "Участники сообщества обсуждали проект НПО и его влияние на рынок.",  # Сокращение НПО
    "Подготовьте доклад по теме 'инж.' и вы получите оценку.",  # Сокращение инж.
    "На встрече также обсуждали вопросы государственной политики в области РСП."  # Сокращение РСП
]

# Пример обработки текста
for text in test_cases:
    print(f"Исходный текст: {text}")

    # Обрабатываем текст
    results = find_and_replace_abbreviations(text)
    if results:
        for result in results:
            print(f"\nТекст после замены: {result['masked_text']}")
            print(f"Сокращение: {result['abbreviation']}")
            print(f"Предсказанное слово: {result['predicted_word']} (вероятность: {result['probability']:.2f})")
    else:
        print("Сокращения не найдены.")
