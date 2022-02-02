from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import json
import math
import random

es = Elasticsearch()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('homepage.html')


@app.route('/search', methods=['GET'])
def search():
    page_size = 15
    keyword = request.args.get('keyword')

    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1
    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                'query': keyword,
                'fields': ['name', 'short_story', 'characters', 'genres','publisher','author'],
                'fuzziness': 1
            }
        }
    }

    res = es.search(index='manga_index', doc_type='', body=body)
    result = []
    if len(res['hits']['hits']) != 0:
        for r in res['hits']['hits']:
            size = len(r['_source']['img_list'])
            img_list = [r['_source']['img_list'][i] for i in random.sample(range(0, size), 3)]
            
            body = {
                'id':          r['_id'],
                'name':        r['_source']['name'],
                'related name': r['_source']['related name'],
                'short_short_story':  r['_source']['short_story'][0:100]+"...",
                'short_story': r['_source']['short_story'],
                'characters':   r['_source']['characters'],
                'genres':      [c.capitalize() for c in r['_source']['genres']],
                'author':      r['_source']['author'],
                'publisher':   r['_source']['publisher'],
                'img':         img_list,
                'score':       r['_score'],
            }
            result.append(body)

    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html', res=result, page_total=page_total, page_no=page_no, keyword=keyword)


@app.route('/manga/<id>')
def manga_page(id):
    arg = id.split('=')
    id = arg[1]
    body = {
        "query": {
            "match": {
                "_id": id
                }
        }
    }
    res = es.search(index='manga_index', doc_type='', body=body)
    # print(res)
    result = {
        'name':         res['hits']['hits'][0]['_source']['name'],
        'related name': '' if res['hits']['hits'][0]['_source']['related name'][0] == '' else res['hits']['hits'][0]['_source']['related name'],
        'short_story':  res['hits']['hits'][0]['_source']['short_story'],
        'characters':   res['hits']['hits'][0]['_source']['characters'],
        'genres':       ', '.join(c.capitalize() for c in res['hits']['hits'][0]['_source']['genres']) ,
        'author':       res['hits']['hits'][0]['_source']['author'],
        'publisher':    res['hits']['hits'][0]['_source']['publisher']
    }
    size = len(res['hits']['hits'][0]['_source']['img_list'])
    rand = random.sample(range(0, size), 1)[0]
    img = res['hits']['hits'][0]['_source']['img_list'][rand]
    return render_template('manga_page.html',res = result, img = img)


if __name__ == '__main__':
    app.run(debug=True)
    # > $env:FLASK_ENV = "development"
