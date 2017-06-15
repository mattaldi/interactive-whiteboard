#!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.set_handle_robots(False)
br.open('http://muhamadaldiansyah.blogspot.com')

response = br.response()
html_doc = response.read()

soup = BeautifulSoup(html_doc, 'html.parser')

##soup = BeautifulSoup(open('http://muhamadaldiansyah.blogspot.com5'))
posts = []
for post in soup.find_all('div', class_='post'):
    title = post.find('h3', class_='post-title').text.strip()
    author = post.find('span', class_='post-author').text.replace('Posted by', '').strip()
##    content = post.find('div', class_='post-body').p.text.strip()
##    date = post.find_previous_sibling('h2', class_='date-header').text.strip()

    posts.append({'title': title})
##                  'author': author,
##                  'content': content,
##                  'date': date})
print posts

