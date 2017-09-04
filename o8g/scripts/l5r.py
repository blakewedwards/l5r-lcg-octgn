def validate_deck():
  mute()
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
      whisper('Only strongholds, roles, and provinces should be in hand.')

  if StrongholdCount != 1:
    ok = False
    whisper('Exactly 1 stronghold should be in hand.')

  if RoleCount > 1:
    ok = False
    whisper('At most 1 role should be in hand.')

  # Provinces
  nameCounts = collections.defaultdict(int)
  ringCounts = collections.defaultdict(int)
  provinces = [c for c in me.hand if c.type == TYPE_PROVINCE]

  if len(provinces) != MAX_PROVINCES:
    ok = False
    whisper('Exactly 5 provinces should be in hand.')

  for card in provinces:
    if card.Clan != 'Neutral' and ClanName != card.Clan:
      ok = False
      whisper('Provinces must be in-clan or neutral, {} is not.'.format(card))

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 1:
      ok = False
      whisper('At most 1 copy of a province may be used, {} has {}.'.format(card, nameCounts[card.name]))

    ringCounts[card.Ring] += 1

    if RoleName == "Seeker of {}".format(card.Ring):
      limit = 2
    else:
      limit = 1

    if ringCounts[card.Ring] > limit:
      ok = False
      whisper('At most {} {} province(s) may be used.'.format(limit, card.Ring))

  # Dynasty deck
  me.piles[DYNASTY].addViewer(me)

  if len(me.piles[DYNASTY]) < 40 or len(me.piles[DYNASTY]) > 45:
    ok = False
    whisper('A dynasty deck must contain a minimum of 40 cards and a maximum of 45.')

  for card in me.piles[DYNASTY]:
    if card.deck != 'Dynasty':
      ok = False
      whisper('A dynasty deck must contain only dynasty cards, {} is not one.'.format(card))

    if card.Clan != 'Neutral' and ClanName != card.Clan:
      ok = False
      whisper('A dynasty deck must contain in-clan or neutral cards, {} is not one.'.format(card))

    if card.name == 'Seeker Initiate' and not RoleName.startswith('Seeker'):
      ok = False
      whisper('Seeker Initiate may only be used with a Seeker role.')

    if card.name == 'Keeper Initiate' and not RoleName.startswith('Keeper'):
      ok = False
      whisper('Keeper Initiate may only be used with a Keeper role.')

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 3:
      ok = False
      whisper('At most 3 copies of a dynasty card may be used, {} has {}.'.format(card, nameCounts[card.name]))

  me.piles[DYNASTY].removeViewer(me)

  # Conflict deck
  me.piles[CONFLICT].addViewer(me)

  if len(me.piles[CONFLICT]) < 40 or len(me.piles[CONFLICT]) > 45:
    ok = False
    whisper('A conflict deck must contain a minimum of 40 cards and a maximum of 45.')

  for card in me.piles[CONFLICT]:
    if card.deck != 'Conflict':
      ok = False
      whisper('A conflict deck must contain only conflict cards, {} is not one.'.format(card))

    if card.type == TYPE_CHARACTER:
      ConflictCharCount += 1

    if card.Clan != 'Neutral' and ClanName != card.Clan:
      if card.properties[INFLUENCE_VALUE] == '':
        ok = False
        whisper('Out-of-clan conflict cards must have an influence cost, {} does not.'.format(card))
      else:
        InfluenceCount += int(card.properties[INFLUENCE_VALUE])

      if InfluenceClanName == '':
        InfluenceClanName = card.Clan
      elif InfluenceClanName != card.Clan:
        ok = False
        whisper('At most 1 clan may be chosen for out-of-clan conflict cards.')

    nameCounts[card.name] += 1

    if nameCounts[card.name] > 3:
      ok = False
      whisper('At most 3 copies of a conflict card may be used, {} has {}.'.format(card, nameCounts[card.name]))

  if ConflictCharCount > 10:
    ok = False
    whisper('At most 10 characters may be included in a conflict deck, found {}.'.format(ConflictCharCount))

  if RoleName.startswith('Keeper'):
    InfluenceLimit = 13
  else:
    InfluenceLimit = 10

  if InfluenceCount > InfluenceLimit:
    ok = False
    whisper('At most {} influence of out-of-clan cards may be included in a conflict deck, found {}.'.format(InfluenceLimit, InfluenceCount))

  me.piles[CONFLICT].removeViewer(me)

  if ok:
    notify("{}'s deck is OK.".format(me))
  else:
    notify("{}'s deck is NOT OK.".format(me))