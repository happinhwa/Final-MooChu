import json
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts=["http://localhost:9200"],
                   headers={"Content-Type": "application/json"})

es.indices.create(
    index='movies',
        settings = {
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
          mappings = {
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
                }
            }
        }

)


with open('./OTT_merged_data.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

body = ""
for x, item in enumerate(json_data):
    id = item['id']
    title_kr = item['title_kr']
    title_En = item['title_En']
    if x %1000==0:
        print(x)

   
    body += json.dumps({"index": {"_index": "movies"}}) + "\n"
    body += json.dumps({"id": id, "title_kr": title_kr,"title_En" : title_En}, ensure_ascii=False) + "\n"

es.bulk(body)