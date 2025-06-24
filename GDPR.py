import requests 
from bs4 import BeautifulSoup 
from langdetect import detect, DetectorFactory 
import re

DetectorFactory.seed = 0  # For consistent language detection results

def audit_page_language_compliance(url):
    report = {
        'url': url,
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

        # 1. Check <html lang="">
        html_tag = soup.find('html')
        if html_tag and html_tag.has_attr('lang'):
            report['html_lang_attr'] = html_tag['lang']
        else:
            report['html_lang_attr'] = 'not set'

        # 2. Detect language from visible text
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        try:
            report['detected_language'] = detect(text[:1000])
        except:
            report['detected_language'] = 'undetected'

        # 3. Search for geo-targeting scripts
        script_text = " ".join([script.get('src', '') + script.text for script in soup.find_all('script')])
        if re.search(r'geo|ipinfo|location|ip-api|geolocation|country', script_text, re.I):
            report['geo_location_script'] = True

        # 4. Check for cookie/consent banners
        banner_text = text.lower()
        if 'cookie' in banner_text or 'gdpr' in banner_text or 'consent' in banner_text:
            report['consent_banner_found'] = True

        # Output result
        print("--- GDPR Language Compliance Report ---")
        for key, value in report.items():
            print(f"{key}: {value}")

    except Exception as e:
        print("Error:", e)

# Example usage
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    audit_page_language_compliance(url)
