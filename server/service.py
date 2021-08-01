from elasticsearch import Elasticsearch

es = Elasticsearch()

index_name = "journal-articles"


def get_source(hit):
    src = hit["_source"].copy()
    src["id"] = hit["_id"]
    highlighted_abstract = hit["highlight"]["abstract"]
    src["abstract"] = (
        highlighted_abstract[0] if len(highlighted_abstract) > 0 else src["abstract"]
    )
    return src


def get_hits_sources(hits):
    return [get_source(hit) for hit in hits]


class JournalService:
    @staticmethod
    def search(query: str):
        try:
            body = {
                "query": {
                    "match_phrase": {
                        "abstract": {
                            "query": query,
                            "slop": 2,
                        }
                    }
                },
                "highlight": {"fields": {"abstract": {}}},
            }

            res = es.search(body=body, index=index_name)
            return get_hits_sources(res["hits"]["hits"])
        except BaseException as e:
            print("error: {}".format(e))
            return []

    @staticmethod
    def get_by_id(id: str):
        try:
            res = es.get(index=index_name, id=id)
            return res["_source"]
        except BaseException as e:
            print("error: {}".format(e))
            return None
