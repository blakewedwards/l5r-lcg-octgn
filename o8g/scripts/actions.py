TYPE_CHARACTER = 'Character'
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
CLAIMED_RINGS = 'Claimed Rings'
STARTING_HAND_SIZE = 4
CARD_GAP_RATIO = 1.0/3.0 # Ratio to width for space inbetween cards
HONOR_DIAL_1 = '4c4f1d22-f2e8-46ff-8446-9aa6ec0a45a6' # Font constantia 24
HONOR_DIAL_CHOICES = 5
IMPERIAL_FAVOR = 'b57c595e-d5ae-4fba-82c8-954a0b78c4a8'
FIRST_PLAYER_TOKEN = 'a88f2213-7711-4699-a94e-23bf10ceedd6'
AIR_RING = '6d19021d-9208-4f3e-8e36-dc2ea28d755e'
EARTH_RING = '7a39169d-1c94-4a2a-9994-105a928dcc7e'
FIRE_RING = '459e0ed9-1dac-4660-b9ba-c0e13bb7db3c'
VOID_RING = '70643b2b-868c-4b2a-84e0-107e0d833ebd'
WATER_RING = 'd5e3fa69-0ab9-4a26-9449-db60ac62e098'
RINGS = [AIR_RING, EARTH_RING, FIRE_RING, VOID_RING, WATER_RING]
RING_X = 304.5 # 3.5 card widths (63) + 4 gaps (1/3 a width)
RING_Y_START = -225
RING_Y_GAP_RATIO = 1
TYPE_ATTACHMENT = 'Attachment'
TYPE_CHARACTER = 'Character'
TYPE_EVENT = 'Event'
TYPE_FIRST_PLAYER_TOKEN = 'First Player Token'
TYPE_HOLDING = 'Holding'
TYPE_HONOR_DIAL = 'Honor Dial'
TYPE_IMPERIAL_FAVOR = 'Imperial Favor'
TYPE_PROVINCE = 'Province'
TYPE_RING = 'Ring'
TYPE_ROLE = 'Role'
TYPE_STRONGHOLD = 'Stronghold'
ALTERNATE_MILITARY = ''
ALTERNATE_POLITICAL = 'Political'
ALTERNATE_CLAIMED = 'Claimed'
MAX_PROVINCES = 5
NUM_HOME_ROWS = 2

def invert_x(x, width, inverted):
  return (-x - width) if inverted else x

def invert_y(y, height, inverted):
  return invert_x(y, height, inverted)

def invert_offset(offset, inverted):
  return offset*(-1 if inverted else 1)

def play_conflict_position(width, height, gap, inverted):
  (x, y) = (-2.5*width - 2*gap + 5*(width+gap), NUM_HOME_ROWS*height + (NUM_HOME_ROWS+1)*gap)
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

def honor_dial_position(width, height, gap, inverted):
  (x, y) = (-4.5*width - 4*gap, NUM_HOME_ROWS*height + (NUM_HOME_ROWS+1)*gap)
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

# The leftmost province is index 0 and will hold the stronghold. Valid indicies are 0 to MAX_PROVINCES-1
def province_position(index, width, height, gap, inverted):
  if index >= MAX_PROVINCES:
    raise ValueError('index must be less than the number of provinces')
  (x, y) = (-2.5*width - 2*gap + index*(width+gap), (NUM_HOME_ROWS*height + (NUM_HOME_ROWS+1)*gap))
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

def role_position(width, height, gap, inverted):
  (x, y) = (-3.5*width - 3*gap, (NUM_HOME_ROWS*height + (NUM_HOME_ROWS+1)*gap))
  return (invert_x(x, width, inverted), invert_y(y, height, inverted))

def height_offset(offset, inverted):
  return offset * (-1 if inverted else 1)

def pass_action(group, x=0, y=0):
  if setup_required(group, x, y):
    return
  notify("{} passes.".format(me))

def is_honor_dial(card, x=0, y=0):
  return unpack(card, lambda c: c.type == TYPE_HONOR_DIAL)

def select_bid(card, x=0, y=0):
  mute()
  if not is_honor_dial(card, x, y):
    return
  notify("{} is selecting their honor bid.".format(me))
  choice = askChoice('Select a bid', [str(c) for c in range(1, HONOR_DIAL_CHOICES + 1)])
  if choice == 0:
    notify('{} did not select a bid.'.format(me))
    return
  else:
    notify('{} has selected a bid.'.format(me))

  if card.isFaceUp:
    card.isFaceUp = False
  card.peek()
  card.alternate = '' if choice == 1 else str(choice)

def gain_honor(honor):
  mute()
  me.honor += honor

def give_honor(group, x=0, y=0):
  mute()
  if setup_required(group, x, y):
    return
  honor = askInteger('Give how much honor?', 0)
  if honor is None:
    return
  if honor == 0:
    return
  if honor > me.honor:
    whisper('Cannot give more honor than available.')
    return
  if len(getPlayers()) == 1:
    whisper('An opponent is required to give honor to.')
    return
  remoteCall(players[1], 'gain_honor', [honor])
  me.honor -= honor
  notify('{} gives {} honor to {}.'.format(me, honor, players[1]))

def setup_required(group, x=0, y=0):
  return bool(me.getGlobalVariable('setup_required'))

def setup_not_required(group, x=0, y=0):
  return not setup_required(group, x, y)

def can_mulligan(group, x=0, y=0):
  return bool(me.getGlobalVariable('can_mulligan')) and not setup_required(group, x, y)

def ring_field(card, field):
  # Currently a bug in OCTGN where cards with alternate have no name, work around it
  alternate = card.alternate
  card.alternate = ''
  name = card.name
  card.alternate = alternate
  return name.lower() + '_' + field

def save_ring_position(card):
  setGlobalVariable(ring_field(card, 'x'), card.position[0])
  setGlobalVariable(ring_field(card, 'y'), card.position[1])

def load_ring_position(card):
  return int(getGlobalVariable(ring_field(card, 'x'))), int(getGlobalVariable(ring_field(card, 'y')))

def setup(group, x=0, y=0):
  mute()
  if not setup_required(group, x, y):
    return
  if not len(me.hand):
    whisper('A deck must be loaded prior to setting up.')
    return

  # There's an extra shuffle here in case they don't use the mulligan action
  me.piles[DYNASTY].shuffle()
  me.piles[CONFLICT].shuffle()

  # Create the stronghold and 4 provinces in a line, with space for a row of cards above. Use the first card dimensions as reference
  width = me.hand[0].width
  height = me.hand[0].height
  gap = width*CARD_GAP_RATIO
  offset = height_offset(gap, me.isInverted)
  if len([c for c in me.hand if c.type != TYPE_STRONGHOLD and c.type != TYPE_PROVINCE and c.type != TYPE_ROLE]) != 0:
    whisper('Set up requires only strongholds, provinces, and roles in hand.')
    return
  stronghold = [c for c in me.hand if c.type == TYPE_STRONGHOLD]
  if len(stronghold) != 1:
    whisper('Set up requires a deck with exactly one stronghold in hand.')
    return
  stronghold = stronghold[0]
  provinces = [c for c in me.hand if c.type == TYPE_PROVINCE]
  if len(provinces) != MAX_PROVINCES:
    whisper('Set up requires a deck with exactly five provinces in hand.')
    return
  role = [c for c in me.hand if c.type == TYPE_ROLE]
  if len(role) > 1:
    whisper('Set up requires a deck with at most one role in hand.')
    return
  role = role[0] if role else None
  i = 0
  while provinces: # Place provinces in random order so not always the same for a deck. Players can select their stronghold province manually
    card = provinces.pop(rnd(0, len(provinces)-1))
    (card_x, card_y) = province_position(i, width, height, gap, me.isInverted)
    card.moveToTable(card_x, card_y, True)
    card.sendToBack()
    card.peek()
    card.anchor = True
    if i == 0:
      stronghold.moveToTable(card_x, card_y + offset)
      stronghold.anchor = True
    i += 1

  if role:
    (card_x, card_y) = role_position(width, height, gap, me.isInverted)
    role.moveToTable(card_x, card_y)
    role.anchor = True

  me.honor = int(stronghold.properties[STARTING_HONOR])
  me.fate += int(stronghold.properties[FATE_VALUE])
  me.setGlobalVariable(PLAYER_FATE_VALUE, stronghold.properties[FATE_VALUE])
  (hd_x, hd_y) = honor_dial_position(width, height, gap, me.isInverted)
  table.create(HONOR_DIAL_1, hd_x, hd_y, persist=True)
  # Shared resources, only set up by one player
  notify('{} sets up.'.format(me))
  if not me.isInverted:
    table.create(IMPERIAL_FAVOR, RING_X+2*width+2*gap, -69/2, persist=True)
    ring_height = 0
    for i, ring_id in enumerate(RINGS):
      ring = table.create(ring_id, RING_X, RING_Y_START + i*ring_height*RING_Y_GAP_RATIO, persist=True)
      ring_height = ring.height
      save_ring_position(ring)

    choice = askChoice('Select the first player', ['Me', 'Opponent', "Kami's choice"])
    if choice != 1 and choice != 2:
      source = 'The Kami choose'
      choice = rnd(1, 2)
    else:
      source = '{} chooses'.format(me)

    first_player = me
    if len(getPlayers()) == 1:
      second_player = None
    else:
      # Get the second player and swap if opponent was chosen
      second_player = [player for player in getPlayers() if player != me][0]
      if choice == 2:
        (first_player, second_player) = (second_player, first_player)

    notify('{} {} as the first player.'.format(source, first_player))
    if second_player:
      second_player.fate += 1

    table.create(FIRST_PLAYER_TOKEN, RING_X+width+gap, gap if first_player == me else -gap-69, persist=True)
  me.setGlobalVariable('setup_required', '')

def mulligan(group, x=0, y=0):
  mute()
  if not can_mulligan(group, x, y):
    return
  notify('{} is mulliganing their dynasty cards.'.format(me))
  me.piles[DYNASTY].shuffle()
  me.piles[CONFLICT].shuffle()
  c = me.piles[DYNASTY].top()
  width = c.width
  height = c.height
  gap = width*CARD_GAP_RATIO
  offset = height_offset(gap, me.isInverted)
  dialog = cardDlg(me.piles[DYNASTY].top(4))
  dialog.title = 'Select dynasty cards to mulligan'
  dialog.min = 0
  dialog.max = 4
  cards = dialog.show()
  if cards is None:
    cards = []
  notify('{} mulligans {} dynasty card(s).'.format(me, len(cards)))
  for card in cards:
    card.moveToBottom(me.piles[DYNASTY])
  for i in range(1, 5):
    c = me.piles[DYNASTY].top()
    (card_x, card_y) = province_position(i, width, height, gap, me.isInverted)
    c.moveToTable(card_x, card_y + offset, True)
  me.piles[DYNASTY].shuffle()
  notify('{} is mulliganing their conflict cards.'.format(me))
  dialog = cardDlg(me.piles[CONFLICT].top(4))
  dialog.title = 'Select conflict cards to mulligan'
  dialog.min = 0
  dialog.max = 4
  cards = dialog.show()
  if cards is None:
    cards = []
  notify('{} mulligans {} conflict card(s).'.format(me,len(cards)))
  for card in cards:
    card.moveToBottom(me.piles[CONFLICT])
  for card in me.piles[CONFLICT].top(4):
    card.moveTo(me.hand)
  me.piles[CONFLICT].shuffle()
  me.setGlobalVariable('can_mulligan', '')

def unpack(item, f, default=True):
  if isinstance(item, list):
    if len(item) != 1:
      return default
    else:
      return f(item[0])
  else:
    return f(item)

def is_province(card, x=0, y=0):
  return unpack(card, lambda c: c.type == TYPE_PROVINCE)

def declare_conflict(group, x=0, y=0):
  mute()
  if setup_required(group, x, y):
    return
  targets = [c for c in group if c.targetedBy == me]
  if len(targets) != 1:
    whisper('A single province must be targeted to declare a conflict.')
    return
  target = targets[0]
  declare_conflict_at(target, x, y)

def declare_conflict_at(card, x=0, y=0):
  mute()
  if not is_province(card):
    whisper('The target of a conflict must be a province.')
    return
  if card.controller == me:
    whisper("The target of a conflict must be an opponent's province.")
    return
  types = ['Military', ALTERNATE_POLITICAL]
  colors = ['#D32E25', '#7E7AD0']
  type = askChoice('Select a type', types, colors)
  if type == 0:
    return
  type = types[type-1]
  unclaimed_rings = [c for c in table if c.type == TYPE_RING and c.alternate != ALTERNATE_CLAIMED]
  dialog = cardDlg(unclaimed_rings)
  dialog.title = 'Select a ring'
  ring = dialog.show()
  if ring is not None:
    ring = ring[0]
    ring.alternate = type if type == ALTERNATE_POLITICAL else ALTERNATE_MILITARY
    ring.target()
    card.target()
    # TODO: Get conflict type
    # TODO: Set ring alternate as contested
    fate = ring.markers[FATE]
    ring.markers[FATE] = 0
    me.fate += fate
    notify('{} declares a {}, {}, conflict against {} and gains {} fate.'.format(me, type.lower(), ring, card, fate))

def set_controller(card, player):
  card.controller = player

def take_control(card):
  if card.controller == me:
    return True
  remoteCall(card.controller, 'set_controller', [card, me])
  return False

def claim_ring(group, x=0, y=0):
  mute()
  if setup_required(group, x, y):
    return
  targets = [c for c in group if c.type == TYPE_RING and c.targetedBy] # Doesn't matter who is targeting, either can claim
  if len(targets) != 1:
    whisper('A single ring must be targeted to be claimed.')
    return
  target = targets[0]
  if take_control(target):
    card_controller_changed(EventArgument({'card': target, 'player': me, 'value': me}))
  # Remaining actions handled in controller changed callback

def card_controller_changed(args):
  # Assume targeted rings that change controller to this player are being claimed
  mute()
  card = args.card
  if card.type == TYPE_RING and card.targetedBy and args.player == me:
    card.target(active=False)
    alternate = card.alternate # Moving to a different group loses the alternate, preserve for rings
    card.moveTo(me.piles[CLAIMED_RINGS])
    card.alternate = alternate
    notify('{} claims the {}.'.format(me, card))

def move_cards(args):
  for i, card in enumerate(args.cards):
    alternate = card.alternate # Preserve the alternate state for rings

    if args.toGroups[i] == table: # Dynasty cards should move to table facedown, unlike conflict which move as faceup
      card.moveToTable(args.xs[i], args.ys[i], True if card.group == me.piles[DYNASTY] else not args.faceups[i])
      card.index = args.indexs[i]
    else:
      card.moveTo(args.toGroups[i], args.indexs[i])

    if card.type == TYPE_RING:
      card.alternate = alternate

def table_default_card_action(card):
  if not card.isFaceUp:
    flip(card)
  else:
    if card.type == TYPE_HONOR_DIAL:
      select_bid(card)
    elif card.type == TYPE_RING or card.type == TYPE_IMPERIAL_FAVOR:
      flip(card)
    elif card.type == TYPE_FIRST_PLAYER_TOKEN:
      pass
    else:
      toggle_bow_ready(card)

def can_honor(card, x=0, y=0):
  return unpack(card, lambda c: c.isFaceUp and c.type == TYPE_CHARACTER)

def honor(card, x=0, y=0):
  if not can_honor(card, x, y):
    return
  if card.markers[DISHONORED]:
    card.markers[DISHONORED] = 0
  elif not card.markers[HONORED]:
    card.markers[HONORED] = 1

def dishonor(card, x=0, y=0):
  if not can_honor(card, x, y):
    return
  if card.markers[HONORED]:
    card.markers[HONORED] = 0
  elif not card.markers[DISHONORED]:
    card.markers[DISHONORED] = 1

def can_fate(card, x=0, y=0):
  return unpack(card, lambda c: c.isFaceUp and (c.type == TYPE_CHARACTER or c.type == TYPE_RING))

def add_fate(card, x=0, y=0, quantity=1):
  if not can_fate(card, x, y):
    return
  card.markers[FATE] += quantity

def remove_fate(card, x=0, y=0):
  if not can_fate(card, x, y):
    return
  card.markers[FATE] -= 1

def can_bow(card, x=0, y=0):
  return unpack(card, lambda c: c.isFaceUp and (c.type == TYPE_CHARACTER or c.type == TYPE_ATTACHMENT or c.type == TYPE_STRONGHOLD))

def toggle_bow_ready(card, x=0, y=0):
  mute()
  if not can_bow(card, x, y):
    return
  card.orientation ^= Rot90
  notify('{} {} {}.'.format(me, 'bows' if card.orientation & Rot90 == Rot90 else 'readies', card))

def toggle_break(card, x=0, y=0):
  mute()
  if not is_province(card, x, y):
    return
  card.orientation ^= Rot180
  notify('{} {} {}.'.format(me, 'breaks' if card.orientation & Rot180 == Rot180 else 'unbreaks', card))

def can_flip(card, x=0, y=0):
  return unpack(card, lambda c: c.type != TYPE_STRONGHOLD and c.type != TYPE_FIRST_PLAYER_TOKEN and c.type != TYPE_ROLE)

def flip(card, x=0, y=0):
  if not can_flip(card, x, y):
    return
  if card.type == TYPE_RING or card.type == TYPE_IMPERIAL_FAVOR:
    card.isFaceUp = True
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

def has_deck(card, x=0, y=0):
  return unpack(card, lambda c: get_pile(c) is not None)

def discard(card, x=0, y=0):
  if not has_deck(card, x, y):
    return
  pile = get_discard_pile(card)
  if pile is not None:
    if card.markers[HONORED]:
      me.honor += 1
    if card.markers[DISHONORED]:
      me.honor -= 1
    card.moveTo(pile)
  return pile

def can_replace(card, x=0, y=0):
  return unpack(card, lambda c: c.type == TYPE_CHARACTER or c.type == TYPE_HOLDING)

def replace(card, x=0, y=0):
  if not can_replace(card, x, y):
    return
  card_x, card_y = card.position
  discard(card, x, y)
  me.piles[DYNASTY].top().moveToTable(card_x, card_y, True)

def refill(card, x=0, y=0):
  if not is_province(card, x, y):
    return
  (x, y) = card.position
  me.piles[DYNASTY].top().moveToTable(x, y + invert_offset(card.width*CARD_GAP_RATIO, me.isInverted), True)

def random_discard_from(group):
  mute()
  card = group.random()
  if card is None:
    return
  pile = discard(card)
  if pile is not None:
    notify("{} randomly moves {} to {}'s {}.".format(me, card, me, pile.name))

def can_play(card, x=0, y=0):
  return unpack(card, lambda c: c.isFaceUp and (c.type == TYPE_CHARACTER or c.type == TYPE_EVENT or c.type == TYPE_ATTACHMENT))

def prompt_reduce_cost(cost):
  reduction = askInteger('Reduce cost by what amount?', 0)
  if reduction is None:
    return
  if reduction > cost:
    reduction = cost
  return cost - reduction

def play_conflict(card, reduced=False):
  mute()
  if card.cost == "":
    whisper('The card does not have a cost.')
    return
  cost = int(card.cost)
  if reduced:
    cost = prompt_reduce_cost(cost)
  if cost is None:
    return
  if me.Fate < cost:
    whisper("The card's cost cannot be paid.")
    return
  num_fate = 0
  if card.type == TYPE_CHARACTER:
    num_fate = prompt_add_fate(cost)
    if num_fate is None:
      return
  (x, y) = play_conflict_position(card.width, card.height, card.width*CARD_GAP_RATIO, me.isInverted)
  card.moveToTable(x, y)
  if card.type == TYPE_ATTACHMENT:
    card.sendToBack()
  me.Fate -= cost + num_fate
  add_fate(card, quantity=num_fate)
  notify_play(me, card, cost, num_fate)

def play_conflict_reduced(card):
  play_conflict(card, reduced=True)

def prompt_add_fate(cost):
  num_fate = askInteger('Add how much fate?', 0)
  if num_fate is None:
    return None
  if me.Fate < cost + num_fate:
    whisper('Only {} fate remains for adding.'.format(me.Fate - cost))
    return None
  return num_fate

def notify_play(player, card, cost, num_fate):
  if num_fate > 0:
    notify('{} plays {} for {} fate and places {} fate on it.'.format(player, card.name, cost, num_fate))
  else:
    notify('{} plays {} for {} fate.'.format(player, card.name, cost))

def play_dynasty(card, x=0, y=0, reduced=False):
  mute()
  if not can_play(card, x, y):
    return
  if not card.isFaceUp:
    whisper('The card is not face up.')
    return
  if card.type != TYPE_CHARACTER:
    whisper('The card is not a character.')
    return
  if card.cost == "":
    whisper('The card does not have a cost.')
    return
  cost = int(card.cost)
  if reduced:
    cost = prompt_reduce_cost(cost)
  if cost is None:
    return
  if me.Fate < cost:
    whisper("The card's cost cannot be paid.")
    return
  num_fate = prompt_add_fate(cost)
  if num_fate is None:
    return
  x, y = card.position
  card.moveToTable(x, y + invert_offset(-card.height - card.width*1.5*CARD_GAP_RATIO, me.isInverted))
  me.Fate -= cost + num_fate
  add_fate(card, quantity=num_fate)
  me.piles[DYNASTY].top().moveToTable(x, y, True)
  notify_play(me, card, cost, num_fate)

def play_dynasty_reduced(card, x=0, y=0):
  play_dynasty(card, x, y, reduced=True)

def resolve_regroup():
  mute()
  cards = (card for card in table if card.controller == me and card.isFaceUp)
  for card in cards:
    card.orientation &= ~Rot90
    if card.type == TYPE_RING:
      add_fate(card)

  me.fate += int(me.getGlobalVariable(PLAYER_FATE_VALUE))
  for card in me.piles[CLAIMED_RINGS]:
    if card.type == TYPE_RING:
      x, y = load_ring_position(card)
      alternate = card.alternate
      card.moveToTable(x, y)
      card.alternate = alternate

def end_turn(group, x=0, y=0):
  mute()
  if setup_required(group, x, y):
    return
  turn = int(getGlobalVariable(TURN))
  if not confirm('Resolve the turn {} regroup phase?'.format(turn)):
    return

  resolve_regroup()
  if len(getPlayers()) != 1:
    remoteCall(players[1], 'resolve_regroup', [])

  # TODO: Test if they have initiative, or don't show the action if not?

  notify('{} resolves the turn {} regroup phase.'.format(me, turn))
  turn += 1
  setGlobalVariable(TURN, str(turn))

def shuffle(group):
  group.shuffle()

def draw(group):
  mute()
  num = askInteger('Draw how many cards?', 1)
  if num is None:
    return
  num = min(num, len(group))
  if num == 0:
    return
  for card in group.top(num):
    card.moveTo(me.hand)
  notify('{} draws {} card(s) from their {}.'.format(me, num, group.name))

def search_top(group, shuffle=False):
  mute()
  num = askInteger('Search how many cards?', 2)
  if num is None:
    return
  num = min(num, len(group))
  if num == 0:
    return

  notify('{} is searching the top {} card(s) of their {}.'.format(me, num, group.name))
  dialog = cardDlg(group.top(num))
  dialog.title = 'Select a card'
  dialog.min = 0
  dialog.max = num
  cards = dialog.show()

  i = 0
  if cards is not None:
    for card in cards:
      (x, y) = play_conflict_position(card.width, card.height, card.width*CARD_GAP_RATIO, me.isInverted)
      card.moveToTable(x + invert_offset(i*(card.width+card.width*CARD_GAP_RATIO), me.isInverted), y, True)
      i += 1
      card.peek()
      card.select()
  else:
    cards = []

  if shuffle:
    group.shuffle()
    notify('{} selects {} card(s) and shuffles their deck.'.format(me, len(cards)))
  else:
    for c in group.top(num-len(cards)):
      c.moveToBottom(group)
    notify('{} selects {} card(s) and moves the remaining to the bottom of their deck.'.format(me, len(cards)))

def search_top_shuffle(group):
  search_top(group, shuffle=True)

def flip_coin(group, x=0, y=0):
  mute()
  if setup_required(group, x, y):
    return
  notify("{} flips a coin and gets {}.".format(me, 'heads' if rnd(1, 2) == 1 else 'tails'))
