from typing import List
from bs4 import BeautifulSoup, ResultSet
from bs4 import element
from .util import get_page_html

class IssueArticle:
  def __init__(self, title, url, authors: List[str], abstract, published_at = '', released_at = ''):
    super().__init__()
    self.title = title
    self.url = url
    self.authors = authors
    self.abstract = abstract
    self.published_at = published_at
    self.released_at = released_at

  def print(self):
    print("{}, {}".format(self.title, self.url))

  def __str__(self):
    return "{}, {}".format(self.title, self.url)

def get_article(soup: element.Tag):
  title_el = soup.find('div', { 'class': 'searchlist-title'})
  title = title_el.get_text().strip()
  url = title_el.findChild('a').get('href')
  authors = soup.find('div', { 'class': 'searchlist-authortags'}).get_text().strip().split(', ')
  p = soup.find('div', { 'class': 'abstract' })
  abstract = '' if p is None else p.get_text().strip()
  if abstract == '':
    print("Warning: cannot find abstract element on {}".format(title))

  article = IssueArticle(
    title, 
    url,
    authors,
    abstract,
  )
  return article 

def get_articles(url):
  html = get_page_html(url)
  soup = BeautifulSoup(markup=html, features='html.parser')
  listing = soup.find('ul', { 'class': 'search-resultslisting' })
  article_els = listing.find_all('li')

  articles = []

  for el in article_els:
    article = get_article(el)
    articles.append(article)
  
  return articles