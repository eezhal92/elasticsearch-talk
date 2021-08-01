#!/usr/bin/env python

from elasticsearch import Elasticsearch
from scrape import get_volumes, get_articles

es = Elasticsearch()

index_name = "journal-articles"


def is_index_exists():
    return es.indices.exists(index_name)


def scrape_journal_articles():
    # get journal articles
    volumes = get_volumes()

    journal_articles = []
    for volume in volumes:
        for issue in volume.issues:
            if issue.url == "":
                continue
            articles = get_articles(issue.url)
            print("{} issue {}:".format(volume.text, issue.text))
            for a in articles:
                print("  article title {}".format(a.title))
                journal_articles.append(a)

    return journal_articles


def create_article_doc(article):
    return {
        "title": article.title,
        "abstract": article.abstract,
        "authors": article.authors,
    }


def index_journal_articles(articles):
    print("trying to index {} articles".format(len(articles)))

    for article in articles:
        doc = create_article_doc(article)
        try:
            res = es.index(index=index_name, body=doc)
            print("indexed: {}".format(res['_id']))
        except Exception as e:
            print("indexing fail for title {}".format(article.title))
            print(e)


if __name__ == "__main__":
    if not is_index_exists():
        raise ValueError(
            "Cannot continue data seeding process. index {} is not exists!".format(
                index_name
            )
        )

    ans = None
    while ans not in ["y", "n"]:
        print("Do you want to scrape articles data and index it? y/n")
        ans = input("Choice: ")
        if ans == "n":
            print("Aborted")
            break
        elif ans == "y":
            print("Scraping journal article data")
            journal_articles = scrape_journal_articles()
            print("Seeding journal article data into elasticsearch")
            index_journal_articles(journal_articles)
        else:
            print("Invalid option")
