from requests_html import HTMLSession

session = HTMLSession()
# r = session.get('https://www.toutiao.com/article/7340206009773883942/?log_from=29ddef388be8_1709562977704',)
r = session.get('https://www.toutiao.com',verify=False)
# print(r.html.text)


# r = session.get('https://example.com')
r.html.render()
print(r.html.text)