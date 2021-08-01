from typing import List
from bs4 import BeautifulSoup, ResultSet
from bs4 import element
from .util import get_page_html

class IssueUrl:
  def __init__(self, text, url):
    super().__init__()
    self.text = text
    self.url = url

class VolumeUrl(IssueUrl):
  def __init__(self, text, url):
    super().__init__(text, url)
    self.issues : List[IssueUrl] = []

  def add_issue(self, issue: IssueUrl):
    self.issues.append(issue)
  
  def set_issues(self, issues: List[IssueUrl]):
    self.issues = issues

  def print(self):
    print(self.text, self.url)
    print('Issues:')
    for issue in self.issues:
      print(' ', issue.text, issue.url)

  def __str__(self):
    return "VolumeUrl({}, {})".format(self.text, self.url)

  def __repr__(self):
    return "VolumeUrl({}, {})".format(self.text, self.url)

def __get_volume_url(section_soup: element.Tag):
  volume_title_el = section_soup.findChild('span', { 'class': 'facetsearch-subheader-link' })
  volume_text = volume_title_el.get_text().strip()
  volume_link = volume_title_el.findChild('a').get('href')
  
  return VolumeUrl(volume_text, volume_link)

def __get_volume_issue_urls(section_soup: element.Tag):
  list_el = section_soup.findAll('li')
  issues = []

  for el in list_el:
    text = el.get_text().strip()
    a = el.findChild('a')
    url = '' if a is None else a.get('href')
    
    issues.append(IssueUrl(text, url))
  
  return issues

def __get_volume_data(soup: element.Tag):
  volume_url = __get_volume_url(soup)
  issue_urls = __get_volume_issue_urls(soup)
  volume_url.set_issues(issue_urls)

  return volume_url

def get_volumes() -> List[VolumeUrl]:
  journal_list_page = 'https://www.jstage.jst.go.jp/browse/irspsd/list/-char/en'
  list_page_html = get_page_html(journal_list_page)
  soup = BeautifulSoup(markup=list_page_html, features="html.parser")  
  volume_sections = soup.find_all('div', { 'class': 'facetsearch-subheader' })

  volumes = []
  for section in volume_sections:
    volume = __get_volume_data(section)
    volumes.append(volume)

  return volumes
