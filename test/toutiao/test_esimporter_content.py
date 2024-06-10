from bs4 import BeautifulSoup


def test_max_increasement_id():
    from elasticsearch import Elasticsearch
    from elastic_transport._transport import TransportApiResponse

    # 创建 Elasticsearch 客户端
    es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme': 'http'}])

    # 定义 SQL 查询
    sql_query = {
        # "query": "SELECT * FROM mytoutiaofav WHERE md_content IS NOT NULL ORDER BY increasement_id DESC LIMIT 1"
        "query": "SELECT max(increasement_id) FROM mytoutiaofav WHERE md_content IS NOT NULL"
    }

    # 执行 SQL 查询
    response:TransportApiResponse = es.transport.perform_request('POST', '/_sql?format=txt', body=sql_query,headers={'Content-Type': 'application/json'},)

    # 打印结果
    print(response.body)


def test_max_increasement_id2():
    from elasticsearch import Elasticsearch

    # 创建 Elasticsearch 客户端
    es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme': 'http'}])

    # 定义查询
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "exists": {
                            "field": "md_content"
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                "increasement_id": {
                    "order": "desc"
                }
            }
        ],
        "size": 1
    }

    # 执行查询
    index_name = "mytoutiaofav"  # 替换为你的实际索引名称
    response = es.search(index=index_name, body=query)

    # 打印结果
    print(response)

    # 解析结果
    if response['hits']['total']['value'] > 0:
        max_record = response['hits']['hits'][0]['_source']
        print("Max increasement_id record:", max_record)
    else:
        print("No records found.")



def test_convert_html_to_markdown():

    import html2text

    # 读取HTML文件
    with open("myfav.html", "r", encoding="utf-8") as file:
        html_content = file.read()


    soup = BeautifulSoup(html_content, 'html.parser')
    article_content = soup.select_one('.article-content')
    wtt_content = soup.select_one('.wtt-content')
    main_content = soup.select_one('.main-content')

    html_content=str(article_content or wtt_content or main_content)



    # 创建html2text对象
    h = html2text.HTML2Text()

    # 设置一些选项
    h.ignore_links = False  # 是否忽略链接
    h.ignore_images = False  # 是否忽略图片

    # 将HTML转换为Markdown
    markdown_content = h.handle(html_content)

    # 打印Markdown内容
    print("Markdown Content:")
    print(markdown_content)

    # 将Markdown内容写入文件
    with open("myfav.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)



def test_convert_html_to_markdown2():

    from markdownify import markdownify as md

    # 读取HTML文件
    with open("myfav.html", "r", encoding="utf-8") as file:
        html_content = file.read()



    soup = BeautifulSoup(html_content, 'html.parser')
    article_content = soup.select_one('.article-content')
    wtt_content = soup.select_one('.wtt-content')
    main_content = soup.select_one('.main-content')

    html_content=str(article_content or wtt_content or main_content)        

    # 将HTML转换为Markdown
    markdown_content = md(html_content)

    # 打印Markdown内容
    print("Markdown Content:")
    print(markdown_content)

    # 将Markdown内容写入文件
    with open("myfav2.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)

if __name__ == '__main__':
    # test_max_increasement_id2()
    # test_convert_html_to_markdown()
    test_convert_html_to_markdown2()