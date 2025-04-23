import sys
import requests
from bs4 import BeautifulSoup

def extract_version(site_url):
    print("[+] البحث عن إصدار WordPress...")
    try:
        r = requests.get(site_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        generator = soup.find('meta', attrs={'name': 'generator'})
        if generator and 'WordPress' in generator.get('content', ''):
            version = generator['content']
            print(f"[✓] إصدار WordPress: {version}")
        else:
            print("[-] لم يتم العثور على إصدار WordPress.")
    except Exception as e:
        print(f"[!] خطأ أثناء الفحص: {e}")

def try_login(site_url, username, password):
    print(f"[+] محاولة تسجيل الدخول باسم: {username} | باسورد: {password}")
    login_url = f"{site_url}/wp-login.php"
    
    session = requests.Session()
    payload = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': f'{site_url}/wp-admin/',
        'testcookie': '1'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'
    }

    try:
        r = session.post(login_url, data=payload, headers=headers, timeout=10)
        if "wp-admin" in r.url or "dashboard" in r.text:
            print(f"[✓] تم الدخول! الباسورد الصحيح هو: {password}")
        else:
            print("[-] فشل تسجيل الدخول، كلمة مرور خاطئة.")
    except Exception as e:
        print(f"[!] خطأ أثناء المحاولة: {e}")

# ----------------------------------
# الاستخدام: python tool.py [site] [-p password] [username]
# ----------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 2:
        site = sys.argv[1].strip().rstrip("/")
        extract_version(site)

    elif len(sys.argv) == 5 and sys.argv[2] == "-p":
        site = sys.argv[1].strip().rstrip("/")
        password = sys.argv[3]
        username = sys.argv[4]
        try_login(site, username, password)

    else:
        print("""
أداة WordPress Info & Login Test by ChatGPT

الاستخدام:
- فحص موقع WordPress:
    python tool.py https://example.com

- تجربة باسورد على يوزر معين:
    python tool.py https://example.com -p PASSWORD USERNAME
""")
