# GDPR-check

Цей Python-скрипт виконує базовий аудит відповідності GDPR для публічних веб-сторінок у контексті мовної доступності та виявлення геолокаційних і згодових елементів.

# Як праює:

1. Завантажує HTML-сторінку за вказаним URL.
2. Витягує атрибут lang з тега <html>.
3. Визначає основну мову сторінки за текстом(до 1000 символів).
4. Перевіряє наявність геолокаційних скриптів.
5. Виявляє банери з повідомленнями про куки/згоду.
6. Зберігає все у JSON-звіт.

# Примітки
1. Через те, що скрипт працює зі статичною HTML-сторінкою, не може обробляти сайти, що довантажують контент динамічно
2. Скрипт не гарантує повний аудит відповідності GDPR, він лише надає попередню оцінку на основі відкритого HTML-коду.
3. Через те, що використовується бібліотека langdetect оцінка мови може бути не точною через перевірку лише перших 1000 символів

# Приклад результату
Тест 1:
--- GDPR Language Compliance Report ---
{
    "url": "https://ecampus.kpi.ua/uk",
    "timestamp": "2025-06-24T10:06:03.014051Z",
    "html_lang_attr": "not set",
    "detected_language": "uk",
    "geo_location_script": false,
    "consent_banner_found": false
}

Тест 2:
--- GDPR Language Compliance Report ---
{
    "url": "https://www.reddit.com/",
    "timestamp": "2025-06-24T10:06:39.738720Z",
    "html_lang_attr": "en-US",
    "detected_language": "en",
    "geo_location_script": true,
    "consent_banner_found": false
}

Тест 3:
--- GDPR Language Compliance Report ---
{
    "url": "https://soundcloud.com/discover",
    "timestamp": "2025-06-24T10:07:11.799918Z",
    "html_lang_attr": "en",
    "detected_language": "en",
    "geo_location_script": true,
    "consent_banner_found": false
}
