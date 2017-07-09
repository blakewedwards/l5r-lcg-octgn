CHARACTER = 'Character'
HONOR = 'Honor'
TURN = 'turn'
STARTING_HONOR = 'Starting Honor'
PLAYER_FATE_VALUE = 'fate_value'
DISHONORED = ('Dishonored', '054b9f42-ac6a-4cc2-9228-294d5df5fb7e')
FATE = ('Fate', '1c469258-900d-44e7-b005-d3c5d0de3f95')
HONORED = ('Honored', 'af5fc343-121e-4ecc-9d21-f3886644b473')
FATE_VALUE = 'Fate Value'
DYNASTY = 'Dynasty Deck'
CONFLICT = 'Conflict Deck'
DYNASTY_DISCARD = 'Dynasty Discard'
CONFLICT_DISCARD = 'Conflict Discard'
STARTING_HAND_SIZE = 4
CARD_GAP_RATIO = 1.0/3.0 # Ratio to width for space inbetween cards
HONOR_DIAL_1 = '4c4f1d22-f2e8-46ff-8446-9aa6ec0a45a6' # Font constantia 24
HONOR_DIAL_CHOICES = 5
AIR_RING = '6d19021d-9208-4f3e-8e36-dc2ea28d755e'
EARTH_RING = '7a39169d-1c94-4a2a-9994-105a928dcc7e'
FIRE_RING = '459e0ed9-1dac-4660-b9ba-c0e13bb7db3c'
VOID_RING = '70643b2b-868c-4b2a-84e0-107e0d833ebd'
WATER_RING = 'd5e3fa69-0ab9-4a26-9449-db60ac62e098'
RINGS = [AIR_RING, EARTH_RING, FIRE_RING, VOID_RING, WATER_RING]
RING_X = 325
RING_Y_START = -225
RING_Y_GAP_RATIO = 1
TYPE_IMPERIAL_FAVOR = 'Imperial Favor'
TYPE_HONOR_DIAL = 'Honor Dial'
TYPE_RING = 'Ring'
ALTERNATE_POLITICAL = 'Political'
MAX_PROVINCES = 5

def invert_x(x, width, inverted):
  return (-x - width) if inverted else x

def invert_y(y, height, inverted):
  return invert_x(y, height, inverted)

def honor_dial_position(width, height, gap, inverted):
  (x, y) = (-3.5*width - 3*gap, height + 3*gap)
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

# The leftmost province is index 0 and will hold the stronghold. Valid indicies are 0 to MAX_PROVINCES-1
def province_position(index, width, height, gap, inverted):
  if index >= MAX_PROVINCES:
    raise ValueError('index must be less than the number of provinces')
  (x, y) = (-2.5*width - 2*gap + index*(width+gap), (height + 2*gap))
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

def height_offset(offset, inverted):
  return offset * (-1 if inverted else 1)

def pass_action(group, x=0, y=0):
  notify("{} passes.".format(me))

def set_honor_dial(group, x=0, y=0):
  mute()
  notify("{} is setting their honor dial.".format(me))
  honor_dial = [card for card in group if card.controller == me and card.type == TYPE_HONOR_DIAL]
  if len(honor_dial) != 1:
    whisper('Error: Honor dial not found.')
    return
  honor_dial = honor_dial[0]
  choice = askChoice('How much honor would you like to bid?', [str(c) for c in range(1, HONOR_DIAL_CHOICES + 1)])
  if choice == 0:
    notify('{} did not select a bid.'.format(me))
    return
  else:
    notify("{} has selected a bid.".format(me))

  if honor_dial.isFaceUp:
    honor_dial.isFaceUp = False
  honor_dial.peek()
  honor_dial.alternate = '' if choice == 1 else str(choice)

def setup_required(group, x=0, y=0):
  return bool(me.getGlobalVariable('setup_required'))

def setup_not_required(group, x=0, y=0):
  return not setup_required(group, x, y)

def setup(group, x=0, y=0):
  mute()
  if not bool(me.getGlobalVariable('setup_required')):
    whisper('Set up is no longer required.')
    return
  if not len(me.hand):
    whisper('A deck must be loaded prior to setting up.')
    return
  # Create the stronghold and 4 provinces in a line, with space for a row of cards above. Use the first card dimensions as reference
  # TODO: isInverted anywhere moved to table
  width = me.hand[0].width
  height = me.hand[0].height
  gap = width*CARD_GAP_RATIO
  offset = height_offset(gap, me.isInverted)
  me.piles[DYNASTY].shuffle()
  me.piles[CONFLICT].shuffle()
  stronghold = me.hand[0] # TODO: If they move the stronghold, this breaks
  for i, card in enumerate(me.hand[1:]):
    (card_x, card_y) = province_position(i, width, height, gap, me.isInverted)
    card.moveToTable(card_x, card_y, True)
    card.sendToBack()
    card.peek()
    card.anchor = True
    if i == 0:
      stronghold.moveToTable(card_x, card_y + offset)
      stronghold.isFaceUp = True
      stronghold.anchor = True
    else:
      me.piles[DYNASTY].top().moveToTable(card_x, card_y + offset, True)

  me.honor = int(stronghold.properties[STARTING_HONOR])
  me.fate = int(stronghold.properties[FATE_VALUE])
  me.setGlobalVariable(PLAYER_FATE_VALUE, stronghold.properties[FATE_VALUE])
  (hd_x, hd_y) = honor_dial_position(width, height, gap, me.isInverted)
  table.create(HONOR_DIAL_1, hd_x, hd_y, persist=True).isFaceUp = True
  for card in me.piles[CONFLICT].top(STARTING_HAND_SIZE):
    card.moveTo(me.hand)
  # TODO: these are shared, not one per player
  table.create('b57c595e-d5ae-4fba-82c8-954a0b78c4a8', 668, 0, persist=True).isFaceUp = True
  ring_height = 0
  for i, ring_id in enumerate(RINGS):
    ring = table.create(ring_id, RING_X, RING_Y_START + i*ring_height*RING_Y_GAP_RATIO, persist=True)
    ring.isFaceUp = True
    ring_height = ring.height
  notify('{} sets up.'.format(me))
  me.setGlobalVariable('setup_required', '')

def table_default_card_action(card):
  if not card.isFaceUp:
    flip(card)
  else:
    toggle_bow_ready(card)

def honor(card, x=0, y=0):
  if card.markers[DISHONORED]:
    card.markers[DISHONORED] = 0
  elif not card.markers[HONORED]:
    card.markers[HONORED] = 1

def dishonor(card, x=0, y=0):
  if card.markers[HONORED]:
    card.markers[HONORED] = 0
  elif not card.markers[DISHONORED]:
    card.markers[DISHONORED] = 1

def add_fate(card, x=0, y=0):
  card.markers[FATE] += 1

def remove_fate(card, x=0, y=0):
  card.markers[FATE] -= 1

def toggle_bow_ready(card, x=0, y=0):
  mute()
  card.orientation ^= Rot90
  notify('{} {} {}.'.format(me, 'bows' if card.orientation & Rot90 == Rot90 else 'readies', card))

def toggle_break(card, x=0, y=0):
  mute()
  card.orientation ^= Rot180
  notify('{} {} {}.'.format(me, 'breaks' if card.orientation & Rot180 == Rot180 else 'unbreaks', card))

def flip(card, x=0, y=0):
  if card.type == TYPE_RING or card.type == TYPE_IMPERIAL_FAVOR:
    card.alternate = ALTERNATE_POLITICAL if not card.alternate else ''
    return
  card.isFaceUp = not card.isFaceUp

def is_dynasty(card):
  return card.size == 'dynasty'

def is_conflict(card):
  return card.size == 'conflict'

def get_pile(card):
  if is_dynasty(card):
    return card.owner.piles[DYNASTY]
  elif is_conflict(card):
    return card.owner.piles[CONFLICT]

def get_discard_pile(card):
  if is_dynasty(card):
    return card.owner.piles[DYNASTY_DISCARD]
  elif is_conflict(card):
    return card.owner.piles[CONFLICT_DISCARD]

def discard(card, x=0, y=0):
  pile = get_discard_pile(card)
  if pile is not None:
    card.moveTo(pile)
  return pile

def move_to_deck_bottom(card, x=0, y=0):
  pile = get_pile(card)
  if pile is not None:
    card.moveToBottom(pile)
  return pile

def replace(card, x=0, y=0):
  card_x, card_y = card.position
  discard(card, x, y)
  me.piles[DYNASTY].top().moveToTable(card_x, card_y, True)

def refill(card, x=0, y=0):
  me.piles[DYNASTY].top().moveToTable(card.position[0], card.position[1] + card.width*CARD_GAP_RATIO, True)

def random_discard_from(group):
  mute()
  card = group.random()
  if card is None:
    return
  pile = discard(card)
  if pile is not None:
    notify("{} randomly moves {} to {}'s {}.".format(me, card, me, pile.name))

def play_conflict(card): #, x=0, y=0):
  mute()
  if card.cost == "":
    whisper('The card does not have a cost.')
    return
  cost=int(card.cost)
  if me.Fate < cost:
    whisper("The card's cost cannot be paid.")
    return
  card.moveToTable(-2.5*card.width - 2*card.width*CARD_GAP_RATIO + 5*(card.width+card.width*CARD_GAP_RATIO), card.height + 2*card.width*CARD_GAP_RATIO, True) # Why True and not False here?
  card.isFaceUp = True
  me.Fate -= cost
  notify('{} plays {} for {} fate.'.format(me, card.name, cost))

def play_dynasty(card, x=0, y=0):
  mute()
  if not card.isFaceUp:
    whisper("The card is not face up.")
    return
  if card.type != CHARACTER:
    whisper("The card is not a character.")
    return
  if card.cost == "":
    whisper('The card does not have a cost.')
    return
  cost=int(card.cost)
  if me.Fate < cost:
    whisper("The card's cost cannot be paid.")
    return
  x, y = card.position
  #TODO: is inverted
  card.moveToTable(x, y - card.height - card.width*2*CARD_GAP_RATIO)
  me.Fate -= cost
  me.piles[DYNASTY].top().moveToTable(x, y, True)
  notify('{} plays {} for {} fate.'.format(me, card.name, cost))

def resolve_regroup():
  mute()
  cards = (card for card in table if card.controller == me and card.isFaceUp)
  for card in cards:
    card.orientation &= ~Rot90
  me.fate += int(me.getGlobalVariable(PLAYER_FATE_VALUE))

def end_turn(table, x=0, y=0):
  mute()
  turn = int(getGlobalVariable(TURN))
  if not confirm('Resolve the turn {} regroup phase?'.format(turn)):
    return

  resolve_regroup()
  if len(getPlayers()) != 1:
    remoteCall(players[1], "resolve_regroup")

  # TODO: Test if they have initiative, or don't show the action if not?

  notify('{} resolves the turn {} regroup phase.'.format(me, turn))
  turn += 1
  setGlobalVariable(TURN, str(turn))

def shuffle(group):
  group.shuffle()

def search_top(group):
  mute()
  num = askInteger('How many cards to search?', 2)
  if num is None:
    return
  num = min(num, len(group))
  if num == 0:
    return

  notify('{} is searching the top {} card(s) of their {}'.format(me, num, group.name))
  dialog = cardDlg(group.top(num))
  dialog.title = 'Select a card'
  dialog.min = 0
  dialog.max = num
  cards = dialog.show()

  if me.isInverted:
    x1 = -150
    y1 = -288
    i = 50
  else:
    x1 = 150
    y1 = 200
    i = -50

  if cards is not None:
    for card in cards:
      card.moveToTable(x1, y1, True)
      x1 += i
      card.peek()
      card.select()
  else:
    cards = []

  for card in group.top(num - len(cards)):
    card.moveToBottom(group)

  notify('{} selected {} cards and put the remaining on the bottom of their deck.'.format(me, len(cards)))

def flip_coin(group, x=0, y=0):
  mute()
  notify("{} flips a coin and gets {}.".format(me, 'heads' if rnd(1, 2) == 1 else 'tails'))
