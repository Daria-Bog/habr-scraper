import requests
from bs4 import BeautifulSoup

# Список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Базовый URL
BASE_URL = 'https://habr.com'

# Заголовки для запросов (чтобы не заблокировали)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Получаем страницу со статьями
response = requests.get(f'{BASE_URL}/ru/articles/', headers=HEADERS)
response.raise_for_status()

# Создаём объект BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все статьи
articles = soup.find_all('article', class_='post_preview')

for article in articles:
    # Дата публикации
    date = article.find('time').text.strip()

    # Заголовок
    title_tag = article.find('h2')
    title = title_tag.text.strip()

    # Ссылка (относительная → абсолютная)
    link = title_tag.find('a')['href']
    if not link.startswith('http'):
        link = BASE_URL + link

    # Preview-текст (в нижнем регистре)
    preview_text = article.text.lower()

    # Проверка ключевых слов в preview
    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        print(f"{date} – {title} – {link}")
        continue  # Если нашли в preview, дальше не проверяем

    # Если в preview нет → проверяем полный текст
    article_resp = requests.get(link, headers=HEADERS)
    article_resp.raise_for_status()
    article_soup = BeautifulSoup(article_resp.text, 'html.parser')

    # Находим полный текст статьи
    article_body = article_soup.find('div', class_='article-formatted-body')
    if article_body:
        full_text = article_body.text.lower()
        if any(keyword.lower() in full_text for keyword in KEYWORDS):
            print(f"{date} – {title} – {link}")
