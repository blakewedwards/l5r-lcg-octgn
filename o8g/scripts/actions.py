HONOR = 'Honor'
STARTING_HONOR = 'Starting Honor'
DYNASTY = 'Dynasty Deck'
CONFLICT = 'Conflict Deck'
DYNASTY_DISCARD = 'Dynasty Discard'
CONFLICT_DISCARD = 'Conflict Discard'
STARTING_HAND_SIZE = 4
CARD_GAP_RATIO = 1.0/3.0 # Ratio to width for space inbetween cards

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
  for i, card in enumerate(me.hand[1:]):
    card.moveToTable(-2.5*width - 2*gap + i*(width+gap), height + 2*gap, True)
    card.sendToBack()
    card.peek()
    card.anchor = True
  stronghold = me.hand[0]
  stronghold.moveToTable(-2.5*width - 2*gap, height + 3*gap)
  stronghold.isFaceUp = True
  stronghold.anchor = True
  me.honor = int(stronghold.properties[STARTING_HONOR])
  me.piles[DYNASTY].shuffle
  me.piles[CONFLICT].shuffle
  for card in me.piles[CONFLICT].top(STARTING_HAND_SIZE):
    card.moveTo(me.hand)
  notify('{} sets up.'.format(me))
  me.setGlobalVariable('setup_required', '')
  return

def table_default_card_action(card):
  if not card.isFaceUp:
    flip(card)
  else:
    toggle_bow_ready(card)

def toggle_bow_ready(card, x=0, y=0):
  mute()
  card.orientation ^= Rot90
  notify('{} {} {}.'.format(me, 'bows' if card.orientation & Rot90 == Rot90 else 'readies', card))

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

def random_discard_from(group):
  mute()
  card = group.random()
  if card is None:
    return
  pile = discard(card)
  if pile is not None:
    notify("{} randomly moves {} to {}'s {}.".format(me, card, me, pile.name))

def play(card): #, x=0, y=0):
  mute()
  if card.cost == "":
    whisper('The card does not have a cost.')
    return
  cost=int(card.cost)
  if me.Fate < cost:
    whisper("The card's cost cannot be paid.")
    return
  card.moveToTable(-2.5*card.width - 2*card.width*CARD_GAP_RATIO + 5*(card.width+card.width*CARD_GAP_RATIO), card.height + 2*card.width*CARD_GAP_RATIO, True)
  card.isFaceUp = True
  me.Fate -= cost
  notify('{} plays {} for {} fate.'.format(me, card.name, cost))
