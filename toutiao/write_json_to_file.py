# coding=utf-8
import json

json1 = {"name": "张三", "age": 30}
json2 = {"name": "李四", "age": 25}
json3 = {"name": "王五", "age": 20}

with open('test.txt', 'a', encoding='utf-8') as f:
    f.write(json.dumps(json1, ensure_ascii=False))
    f.write('\n')

with open('test.txt', 'a', encoding='utf-8') as f:
    f.write(json.dumps(json2, ensure_ascii=False))
    f.write('\n')

with open('test.txt', 'a', encoding='utf-8') as f:
    f.write(json.dumps(json3, ensure_ascii=False))
    f.write('\n')
