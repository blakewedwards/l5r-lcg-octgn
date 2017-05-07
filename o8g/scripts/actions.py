HONOR = 'Honor'
STARTING_HONOR = 'Starting Honor'
DYNASTY = 'Dynasty Deck'
CONFLICT = 'Conflict Deck'
STARTING_HAND_SIZE = 4
CARD_GAP_RATIO = 1.0/3.0 # Ratio to width for space inbetween cards

def setup_required(table, x, y):
  return bool(me.getGlobalVariable('setup_required'))

def setup(table, x, y):
  mute()
  if not bool(me.getGlobalVariable('setup_required')):
    notify('Set up is no longer required')
    return
  if not len(me.hand):
    notify('You must load a deck prior to setting up')
    return
  # Create the stronghold and 4 provinces in a line, with space for a row of cards above. Use the first card dimensions as reference
  # TODO: isInverted
  width = me.hand[0].width
  height = me.hand[0].height
  gap = width * CARD_GAP_RATIO
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
  notify('{} sets up'.format(me))
  me.setGlobalVariable('setup_required', '')
  return

def table_default_card_action(card):
  if not card.isFaceUp:
    card.isFaceUp=True
  else:
    mute()
    card.orientation ^= Rot90
    notify('{} {} {}.'.format(me, 'bows' if card.orientation & Rot90 == Rot90 else 'readies', card))
