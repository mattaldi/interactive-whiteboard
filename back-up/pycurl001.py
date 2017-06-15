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

##
##
####html_doc = """
####<html><head><title>The Dormouse's story</title></head>
####<body>
####<p class="title"><b>The Dormouse's story</b></p>
####
####<p class="story">Once upon a time there were three little sisters; and their names were
####<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
####<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
####<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
####and they lived at the bottom of a well.</p>
####
####<p class="story">...</p>
####"""
##print(soup.prettify())
##
