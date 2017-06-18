CHARACTER = 'Character'
HONOR = 'Honor'
TURN = 'turn'
STARTING_HONOR = 'Starting Honor'
PLAYER_FATE_VALUE = 'fate_value'
FATE = ('Fate', '1c469258-900d-44e7-b005-d3c5d0de3f95')
FATE_VALUE = 'Fate Value'
DYNASTY = 'Dynasty Deck'
CONFLICT = 'Conflict Deck'
DYNASTY_DISCARD = 'Dynasty Discard'
CONFLICT_DISCARD = 'Conflict Discard'
STARTING_HAND_SIZE = 4
CARD_GAP_RATIO = 1.0/3.0 # Ratio to width for space inbetween cards
HONOR_DIAL_1 = '4c4f1d22-f2e8-46ff-8446-9aa6ec0a45a6' # Font constantia 24
HONOR_DIAL_CHOICES = 5

def set_honor_dial(group, x=0, y=0):
  mute()
  notify("{} is setting their honor dial.".format(me))
  honor_dial = [card for card in group if card.controller == me and card.type == 'Honor Dial']
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
  me.piles[DYNASTY].shuffle
  me.piles[CONFLICT].shuffle
  for i, card in enumerate(me.hand[1:]):
    card.moveToTable(-2.5*width - 2*gap + i*(width+gap), height + 2*gap, True)
    if i > 0:
      me.piles[DYNASTY].top().moveToTable(-2.5*width - 2*gap + i*(width+gap), height + 3*gap, True)
    card.sendToBack()
    card.peek()
    card.anchor = True
  stronghold = me.hand[0]
  stronghold.moveToTable(-2.5*width - 2*gap, height + 3*gap)
  stronghold.isFaceUp = True
  stronghold.anchor = True
  me.honor = int(stronghold.properties[STARTING_HONOR])
  me.fate = int(stronghold.properties[FATE_VALUE])
  me.setGlobalVariable(PLAYER_FATE_VALUE, stronghold.properties[FATE_VALUE])
  table.create(HONOR_DIAL_1, -3.5*width - 3*gap, height + 3*gap, persist=True).isFaceUp = True
  for card in me.piles[CONFLICT].top(STARTING_HAND_SIZE):
    card.moveTo(me.hand)
  notify('{} sets up.'.format(me))
  me.setGlobalVariable('setup_required', '')
  table.create('b57c595e-d5ae-4fba-82c8-954a0b78c4a8', 668, 0, persist=True)

def table_default_card_action(card):
  if not card.isFaceUp:
    flip(card)
  else:
    toggle_bow_ready(card)

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
  card.isFaceUp = not card.isFaceUp

def is_dynasty(card):
  return card.size == 'dynasty'

def is_conflict(card):
  return card.size == 'conflict'

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
