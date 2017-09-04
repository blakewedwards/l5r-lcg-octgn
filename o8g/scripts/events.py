def on_deck_loaded(args):
  if args.player != me: # TODO: Have the other player validate or both validate?
    return
  # TODO: Use groups
  validate_deck()
