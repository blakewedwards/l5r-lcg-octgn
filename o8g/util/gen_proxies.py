#!/usr/bin/env python
import itertools
import os
import sys
from xml.dom.minidom import parse

if (len(sys.argv) != 2):
  sys.exit('Usage: {} <deck.o8d>'.format(os.path.basename(sys.argv[0])))

# Get ids and quantities for cards in the deck
cards = [(card.getAttribute('id'), int(card.getAttribute('qty'))) for card in parse(sys.argv[1]).getElementsByTagName('card')]

# Expand the ids to have each appearing a number of times equal to its quantity
ids = [i for (id, qty) in cards for i in itertools.repeat(id, qty)]

# Organize the ids into rows/columns
num_columns = 3
rows = [ids[i:i+num_columns] for i in range(0, len(ids), num_columns)]

# Htmlify. Td has left/right padding to balance the whitespace chrome automatically adds to the bottom. Width is specified as 240 in
# case all downloaded images aren't the same size.
print """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<style>img {{width: 240px;}} table {{border-spacing: 0px;}} td {{padding: 0 1px 0 1px;}}</style>
</head>
<body>
<table>
<tr>
{}
</tr>
</table>
</body>
</html>""".format("\n</tr>\n<tr>\n".join(["<td>{}</td>".format("</td>\n<td>".join(['<img src="{}.png"/>'.format(id) for id in row])) for row in rows]))
