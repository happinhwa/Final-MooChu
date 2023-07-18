import json
from elasticsearch import Elasticsearch


es = Elasticsearch()

es.indices.create(
    index='movies',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
          "mappings": {
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "title_kr": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "title_En": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "actors": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "media_type": {
                    "type": "keyword"
                },
                "poster_image_url": {
                    "type": "text"
                },
                "genres": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
            }
        }

    }
)


with open('./Movie1.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

body = ""
for x, item in enumerate(json_data):
    id = item['id']
    title_kr = item['title_kr']
    poster_image_url= item['poster_image_url']
    title_En = item['title_En']
    actor = "배우" 
    genres= item['genres']
    print(x)

   
    body += json.dumps({"index": {"_index": "movies"}}) + "\n"
    body += json.dumps({"id": id, "title_kr": title_kr,"poster_image_url":poster_image_url,"title_En" : title_En,"actor": actor,"genres":genres}, ensure_ascii=False) + "\n"

es.bulk(body)