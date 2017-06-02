import itertools
from xml.dom import minidom

file = 'deck.o8d'

dom = minidom.parse(file)
cards = [(card.getAttribute('id'), int(card.getAttribute('qty'))) for card in dom.getElementsByTagName('card')]

class row_builder:
  def __init__(self):
    self.row_count = 0
    self.rows = [[]]

  def append(self, image_src):
    self.rows[-1].append(image_src)
    if len(self.rows[-1]) == 3:
      self.rows.append([])

s = "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\">\n<html><head><style>img {width: 220px;}</style>\n</head>\n\n<body>\n<table>\n<tr>"
r = row_builder()
for (id, qty) in cards:
  for _ in itertools.repeat(None, qty):
    r.append(id)

s += '</tr><tr>'.join(['<td>' + '</td><td>'.join(['<img src="' + id + '.png">' for id in row]) + '</td>' for row in r.rows])
s += "</tr>\n</table>\n</body>\n</html>";
print s
