Dynasty = 'Dynasty Deck'
Conflict = 'Conflict Deck'
StartingHandSize = 5

def setup_required(table, x, y):
  return bool(me.getGlobalVariable('setup_required'))

def setup(table, x, y):
  if not bool(me.getGlobalVariable('setup_required')):
    notify('Set up is no longer required')
    return
  if not len(me.hand):
    notify('You must load a deck prior to setting up')
    return
  me.hand[0].moveToTable(0, 0)
  for card in me.hand:
    card.moveToTable(0, 0, True)
  me.piles[Dynasty].shuffle
  me.piles[Conflict].shuffle
  for card in me.piles[Conflict].top(StartingHandSize):
    card.moveTo(me.hand)
  notify('{} sets up'.format(me))
  me.setGlobalVariable('setup_required', '')
  return
