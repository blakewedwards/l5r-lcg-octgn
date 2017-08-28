# l5r-lcg-octgn
OCTGN plugin for Legend of the Five Rings: The Card Game

## Installation

Currently there isn't a feed with this game, manual installation using the local feed is required. Pre-built versions can be found under [releases](https://github.com/blakewedwards/l5r-lcg-octgn/releases) or in the [drive](https://drive.google.com/drive/folders/0By_ODAjR2bBEX1RZZjM0UEdHQVE). It's recommended to use the pre-built versions due to how OCTGN manages the updates for a game when a new version is found in a feed.

1. Download the latest game package (Legend of the Five Rings LCG-\*.\*.\*.\*.nupkg) from one of the sources above
1. Copy/move the downloaded game package to your OCTGN local feed directory (typically "C:\Users\\%USERNAME%\Documents\OCTGN\LocalFeed")
1. (Re)start OCTGN
1. Select the **Games Manager** tab
1. Select **Local (Developers)** from the dropdown in the top left of the tab
1. Select **Legent of the Five Rings LCG** from the list and click the **Install** button
1. You can optionally add an image pack by selecting **Add Image Packs** (a few buttons right of the feed dropdown) and navigating to the image pack you've made/obtained
1. The game should now be installed and availabe in the deck editor or when starting a new game

## Updating

If a new version has been released since you first installed the game, obtain the latest version as per **Installation** and copy/move it to the local feeds directory. When starting OCTGN, it should automatically detect and update to the latest version.

## Guide

Most game objects can be interacted with by single/double clicking or dragging them between groups. To simplify common steps, actions are associated with different game objects and can be seen in a menu by alt-clicking (typically right mouse button) the game object. Card groups and the table also have actions that can be accessed in the same way. Some actions expect or will automatically perform the targeting of a card (shift+click).

1. Build a deck in the deck editor, cards should be added to the correct section for setup to work correctly.
1. Start or join a game and load your deck. After loading your deck you should see your stronghold, provinces, and optionally a role in your hand. To the right of your hand is your **Conflict Deck**, **Conflict Discard**, **Dynasty Deck**, **Dynasty Discard**, and **Claimed Rings** (defaults as collapsed but can be clicked to expand)
1. Both players **Setup** (select the **Setup** action by alt-clicking the table). After setup your provinces will be randomly placed in a line on the table
1. Both players **Mulligan** (select the **Mulligan** action by alt-clicking the table). This sequence will allow you to select dynasty and conflict cards to mulligan and end with your provinces populated and your starting hand visible. Once both players have completed their mulligan, each can select their dynasty cards and double click to flip
1. Most game objects can be interacted with by clicking, dragging, or selecting one of their actions with alt-click. To simplify steps that interact with multiple game objects, actions have been associated with the table (alt-click the table itself)
    * Pass - indicate you have nothing to trigger when it's your priority
    * Give honor - exchange honor as part of resolving honor dial selection
    * Declare conflict - after targeting an opponent's province with shift+click, use this to choose a type and ring for a conflict
    * Claim ring - after completing a conflict, the winner can use this to claim the ring
    * End turn - ends the turn by adding a fate to each unclaimed ring and readies all characters
