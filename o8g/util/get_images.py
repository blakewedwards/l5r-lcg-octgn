from HTMLParser import HTMLParser
import os
import shutil
import sys
from urllib2 import HTTPError, Request, urlopen
from xml.dom.minidom import parse

if (len(sys.argv) != 3):
  sys.exit('Usage: {} <set.xml> <output_folder>'.format(os.path.basename(sys.argv[0])))

class PNGPageParser(HTMLParser):
  def __init__(self, name):
    HTMLParser.__init__(self)
    self.image_url = ''
    self.file = False

  def handle_starttag(self, tag, attrs):
    if tag == 'div':
      self.file = ('id', 'file') in attrs
    elif tag == 'img' and self.file:
      self.image_url = [value for (name, value) in attrs if name == 'src'][0].strip().replace('https://', 'http://')

  def handle_endtag(self, tag):
    if tag == 'div':
      self.file = False

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
name_swaps = {'Yojin no Shiro': 'Shiro no Yojin'}
jpgs = ['Deathseeker']
cards = [(card.getAttribute('name'), card.getAttribute('id')) for card in parse(sys.argv[1]).getElementsByTagName('card')]
not_found = []
for (name, id) in cards:
  name = name_swaps.get(name, name)
  url = 'http://l5r.gamepedia.com/File:{}.{}'.format(name.replace(' ', '_'), 'jpg' if name in jpgs else 'png')
  try:
    parser = PNGPageParser(name)
    print 'GET ' + url
    parser.feed(urlopen(Request(url, None, {'User-Agent': user_agent})).read())
    parser.close()
    if parser.image_url:
      print '  GET ' + parser.image_url
      with open(os.path.join(sys.argv[2], id) + '.png', 'wb') as image:
        shutil.copyfileobj(urlopen(parser.image_url), image)
    else:
      not_found.append(name)
  except HTTPError as err:
    print '  ' + str(err)
    not_found.append(name)

print 'Not found: ' + str(not_found)
