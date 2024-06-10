

from bs4 import BeautifulSoup
from markdownify import markdownify as md

def convert_html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article_content = soup.select_one('.article-content')
    wtt_content = soup.select_one('.wtt-content')
    main_content = soup.select_one('.main-content')

    html_content=str(article_content or wtt_content or main_content or html_content)        

    markdown_content = md(html_content)
    return markdown_content