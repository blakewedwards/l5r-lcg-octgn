def validate_deck():
  mute()
  notify (" -> Checking deck of {} ...".format(me))
  ok = True
  StrongholdCount = 0
  RoleCount = 0
  ProvinceCount = 0
  InfluenceCount = 0
  ConflictCharCount = 0
  ClanName = ''
  RoleName = ''
  InfluenceClanName = ''

  for card in me.hand:
    if card.type == TYPE_STRONGHOLD:
      StrongholdCount += 1
      ClanName = card.Clan
    elif card.type == TYPE_ROLE:
      RoleCount += 1
      RoleName = card.Name
    elif card.type != TYPE_PROVINCE:
      ok = False
      whisper("You have a card in your hand that is not a stronghold, role or province, please put it in the appropriate deck.")

  if StrongholdCount != 1:
    ok = False
    whisper("You should have exactly 1 stronghold card in your hand.")
  if RoleCount > 1:
    ok = False
    whisper("You can only use 1 role.")

  #Provinces
  nameCounts = collections.defaultdict(int)
  ringCounts = collections.defaultdict(int)
  provinces = [c for c in me.hand if c.type == TYPE_PROVINCE]

  if len(provinces) != MAX_PROVINCES:
    ok = False
    whisper("You must have exactly 5 provinces.")

  for card in provinces:
    if card.Clan != 'Neutral' and ClanName not in card.Clan:
      ok = False
      notify("{}'s provinces contain a card from another clan. Name is {}.".format(me,card))

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 1:
      ok = False
      notify("{} has {} copies of {}, but can have only 1.".format(me, nameCounts[card.name], card))

    ringCounts[card.Ring] += 1

    if RoleName == "Seeker of {}".format(card.Ring):
      limit = 2
    else:
      limit = 1

    if ringCounts[card.Ring] > limit:
      ok = False
      notify("{} has {} {} provinces, but can have only {}".format(me, ringCounts[card.Ring], card.Ring, limit))

  #Dynasty deck
  me.piles[DYNASTY].addViewer(me)

  if len(me.piles[DYNASTY]) < 40:
    ok = False
    notify("{}'s dynasty deck must contain at least 40 cards".format(me))
  if len(me.piles[DYNASTY]) > 45:
    ok = False
    notify("{}'s dynasty deck must contain at most 45 cards".format(me))

  for card in me.piles[DYNASTY]:
    if card.type != TYPE_CHARACTER and card.type != TYPE_HOLDING:
      ok = False
      notify("{}'s dynasty deck must contain only characters and holdings. Name is {}.".format(me,card))

    if card.Clan != 'Neutral' and ClanName not in card.Clan:
      notify("{}'s dynasty deck contain a card from another clan. Name is {}.".format(me,card))

    if card.name == 'Seeker Initiate' and not RoleName.startswith('Seeker'):
      ok = False
      notify("Seeker Initiate requires a Seeker role.")

    if card.name == 'Keeper Initiate' and not RoleName.startswith('Keeper'):
      ok = False
      notify("Keeper Initiate requires a Keeper role.")

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 3:
      ok = False
      notify("{} has {} copies of {}, but can have only 3.".format(me, nameCounts[card.name], card))

  me.piles[DYNASTY].removeViewer(me)

  #Conflict deck
  me.piles[CONFLICT].addViewer(me)

  if len(me.piles[CONFLICT]) < 40:
    ok = False
    notify("{}'s conflict deck must contain at least 40 cards".format(me))
  if len(me.piles[CONFLICT]) > 45:
    ok = False
    notify("{}'s conflict deck must contain at most 45 cards".format(me))

  for card in me.piles[CONFLICT]:
    if card.type != TYPE_CHARACTER and card.type != TYPE_ATTACHMENT and card.type != TYPE_EVENT:
      ok = False
      notify("{}'s conflict deck must contain only characters, attachments and events. Name is {}.".format(me,card))

    if card.type == TYPE_CHARACTER:
      ConflictCharCount += 1

    if card.Clan != 'Neutral' and ClanName not in card.Clan:
      if card.properties[INFLUENCE_VALUE] == '':
        ok = False
        notify("{}'s conflict deck contains an out-of-clan card with no influence cost. Name is {}.".format(me,card))
      else:
        InfluenceCount += int(card.properties[INFLUENCE_VALUE])

      if InfluenceClanName == '':
        InfluenceClanName = card.Clan
      elif InfluenceClanName not in card.Clan:
        notify("{}'s conflict deck contains out-of-clan cards from more than 1 clan.".format(me))

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 3:
      ok = False
      notify("{} has {} copies of {}, but can have only 3.".format(me, nameCounts[card.name], card))

    if ConflictCharCount > 10:
     ok = False
     notify("{}'s conflict deck contains {} character, but can have only 10".format(me, ConflictCharCount))

  if RoleName.startswith('Keeper'):
    InfluenceLimit = 13
  else:
    InfluenceLimit = 10

  if InfluenceCount > InfluenceLimit:
    ok = False
    notify("{}'s conflict deck contains out-of-clan cards with {} influence, but can have only {}".format(me, InfluenceCount, InfluenceLimit))
  me.piles[CONFLICT].removeViewer(me)

  if ok:
    notify("Deck of {} is OK".format(me))
  else:
    notify("Deck of {} is NOT OK".format(me))