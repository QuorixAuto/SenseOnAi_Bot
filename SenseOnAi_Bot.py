import requests
from bs4 import BeautifulSoup

# 발급받은 텔레그램 토큰과 챗 ID
TELEGRAM_TOKEN = "8889201900:AAHGcoG-ablPOj7L2FW-EavsnAWmvKHG15A"
CHAT_ID = "8803567047"

# 타깃 주식 종목 코드
TARGET_STOCKS = {
    "SK증권": "001510",
    "SK하이닉스": "000660",
    "SFA반도체": "036540"
}

def get_stock_price(code):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # 네이버 금융에서 현재가 크롤링
    price = soup.select_one('.no_today .blind').text
    return price

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def main():
    message = "📈 현재 타깃 종목 시세 알림\n\n"
    for name, code in TARGET_STOCKS.items():
        try:
            price = get_stock_price(code)
            message += f"✔️ {name}: {price}원\n"
        except Exception as e:
            message += f"❌ {name}: 데이터 수집 실패\n"
            
    send_telegram_message(message)
    print("텔레그램 알림 전송 완료!")

if __name__ == "__main__":
    main()