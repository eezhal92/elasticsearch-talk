from urllib.request import urlopen

def get_page_html (url: str):
  page = urlopen(url)
  return page.read().decode('utf-8')