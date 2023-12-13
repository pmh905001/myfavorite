import json
import sqlite3


def read_lines():
    with open('toutiao-myfavorites.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines


def insert(conn, page: str):
    infos = list(reversed(json.loads(page).get('data', [])))
    if infos:
        records = [json.dumps(r, ensure_ascii=False) for r in infos]
        conn.execute('insert into toutiao (info) values ' + ','.join(['(?)'] * len(infos)), records)
    conn.commit()


def import_to_sqlite():
    conn = sqlite3.connect(r'..\myfav.db')
    lines = read_lines()
    pages = list(reversed(lines))
    for index, page in enumerate(pages):
        print(f'page: {index}')
        insert(conn, page)
    conn.close()


if __name__ == '__main__':
    import_to_sqlite()
