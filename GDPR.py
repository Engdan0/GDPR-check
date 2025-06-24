import requests
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
import re
import json
from datetime import datetime

DetectorFactory.seed = 0  # стабільний результат

def audit_page_language_compliance(url):
    report = {
        'url': url,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'html_lang_attr': '',
        'detected_language': '',
        'geo_location_script': False,
        'consent_banner_found': False
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. <html lang="">
        html_tag = soup.find('html')
        report['html_lang_attr'] = html_tag.get('lang', 'not set') if html_tag else 'not found'

        # 2. Виявлення мови тексту
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        try:
            report['detected_language'] = detect(text[:1000])
        except:
            report['detected_language'] = 'undetected'

        # 3. Геолокаційні скрипти
        script_text = " ".join([script.get('src', '') + script.text for script in soup.find_all('script')])
        if re.search(r'geo|ipinfo|location|ip-api|geolocation|country', script_text, re.I):
            report['geo_location_script'] = True

        # 4. Пошук банера згоди
        banner_text = text.lower()
        if any(keyword in banner_text for keyword in ['cookie', 'consent', 'gdpr']):
            report['consent_banner_found'] = True

        # Виведення
        print("--- GDPR Language Compliance Report ---")
        print(json.dumps(report, indent=4, ensure_ascii=False))

        # Збереження у JSON-файл
        with open('gdpr_audit_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print("Error:", e)

# Запуск
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    audit_page_language_compliance(url)
