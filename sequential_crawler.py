from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin, urlparse
import nltk
from nltk.corpus import stopwords

response = urllib.request.urlopen('https://github.com/')
root_url = "https://github.com/"

html = response.read()

soup = BeautifulSoup(html, "lxml")

text = soup.get_text(strip='true')
# print(text)

links = soup.find_all('a', href=True)
# print(links)

outlinks = []

for link in links:
    url = link['href']
    print("\nScrapping URL: {}\n".format(url))
    if url.startswith('/') or url.startswith(root_url):
        url = urljoin(root_url, url)
        outlinks.insert(1, url)

tokens = [t for t in text.split()]

print("\nNumber Of Tokens: {}\n".format(len(tokens)))

clean_tokens = tokens[:]

sr = stopwords.words('english')

for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)

print("Tokens after stop words removal \n", clean_tokens)
print(len(clean_tokens))

print("no of stopwords =\n", len(tokens) - len(clean_tokens))

freq = nltk.FreqDist(clean_tokens)
print("\n Frequency", freq, "\n")
print(freq.items())

for key, val in freq.items():
    print(str(key) + ':' + str(val))
