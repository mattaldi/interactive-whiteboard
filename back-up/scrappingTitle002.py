import urllib2  
from bs4 import BeautifulSoup  
import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)
br.open('https://futurism.com/')

response = br.response()
html_doc = response.read()

soup = BeautifulSoup(html_doc, 'html.parser')

##name_box = soup.find_all('h3', attrs={'class': 'post-title'})

##name = name_box.text.strip()

##posts = []
##for post in soup.find_all('div', class_='post'):
##    title = post.find('h3', class_='post-title').text.strip()
##    author = post.find('span', class_='post-author').text.replace('Posted by', '').strip()
