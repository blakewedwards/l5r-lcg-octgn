import urllib2
from HTMLParser import HTMLParser  

class MyHTMLParser(HTMLParser):

  def __init__(self, name):
    HTMLParser.__init__(self) 
    self.image_urls = []
    self.file = False

  def handle_starttag(self, tag, attrs):
    if tag == 'div':
      for name, value in attrs:
        if name == 'id' and value == 'file':
          self.file = True

    if tag == 'img' and self.file:
      src = ''
      found = False
      for name, value in attrs:
        if name == 'src':
          src = value
        elif name == 'alt' and value == 'File:' + name + '.png':
          found = True

      self.image_urls.append(src)
      
  def handle_endtag(self, tag):
    if tag == 'div':
      self.file = False
      
name = 'Above Question'
req = urllib2.Request(url='https://l5r.gamepedia.com/File:' + name.replace(' ', '_') + '.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
f = urllib2.urlopen(req)
p = MyHTMLParser(name)
html = f.read()
p.feed(html)
for image_url in p.image_urls:
  with open(name + '.png', 'wb') as f:
    print image_url
    f.write(urllib2.urlopen(image_url).read())
p.close()
