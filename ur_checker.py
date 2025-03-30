import os
import requests
from bs4 import BeautifulSoup

LINE_TOKEN = os.getenv('LINE_TOKEN')

UR_URLS = {
    '千代田区': 'https://www.ur-net.go.jp/chintai/kanto/tokyo/area/101.html',
    '中央区':   'https://www.ur-net.go.jp/chintai/kanto/tokyo/area/102.html'
}

def send_line_notify(message):
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    data = {'message': message}
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)
    if r.status_code != 200:
        print("通知失敗:", r.text)

def fetch_vacant_properties():
    vacant = []
    for ward, url in UR_URLS.items():
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('.mod-searchResultList-item'):
            title = item.find('h3').get_text(strip=True)
            status_tag = item.select_one('.mod-searchResultList-itemStatus')
            if status_tag and '空室あり' in status_tag.get_text():
                link_tag = item.find('a')
                href = link_tag['href'] if link_tag else ''
                full_url = href if href.startswith('http') else f"https://www.ur-net.go.jp{href}"
                vacant.append((f"{ward}：{title}", full_url))
    return vacant

def main():
    props = fetch_vacant_properties()
    if not props:
        print("空室なし")
    for title, url in props:
        send_line_notify(f"【新着空室】\n{title}\n{url}")

if __name__ == '__main__':
    main()
