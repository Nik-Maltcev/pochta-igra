# Mouseproof Mailroom 📦🐭

A quick postal warehouse puzzle for desktop and mobile. Pick a parcel card, place it on an open shelf, seal rows and columns with four different parcel types, make matching 2×2 patches, and catch mice before they chew the delivery. Your first shift starts with three parcels already sorted, so one move teaches the main scoring rule.

## Play locally

Open `index.html` in a browser, or serve this folder with a local web server and visit `http://localhost:8765/`. No build step or package install is needed. The game remains playable if the CrazyGames SDK cannot load.

## Controls and scoring

- Tap or click a card, then an empty shelf. On desktop, keys `1`, `2`, and `3` select cards.
- The first shift shows a glowing shelf and short tips. Use the `?` button to hide or restore tips.
- Use **Reroute Hand** once per shift to trade all three cards for fresh ones. On desktop, press `R`.
- Each parcel you deliver earns **1 point**. Score **70 points** before the shift ends to clear the route.
- A row or column of four different parcels seals for **10 points**. Completing both at once adds another **10 points**.
- A 2×2 block of one parcel type makes a patch for **4 points**.
- Placing a parcel on a mouse catches it for **5 points**. Uncaught mice cost **5 points** at the end; hungry mice can chew unprotected parcels.
- Three short missions are drawn each shift, worth **10 points** each. A shift ends when the counter reaches **16 sorted parcels**; the first shift has three parcels already on the shelves. Your best score is saved.
- Earning seal, patch, or mouse bonuses on consecutive deliveries builds a combo: **+3**, then **+6**, up to **+9** per turn. Five collectible stamps reward different achievements and stay unlocked between visits.

## CrazyGames upload

Upload `index.html` and `styles.css` together as the HTML5 game files in the CrazyGames Developer Portal. The v3 SDK initializes on CrazyGames and localhost, with gameplay start/stop, audio settings, game completion, high-score celebration, cloud-backed best score and stamps through the Data module, and a midgame ad request at a completed shift after at least three minutes of play. Select **Yes, using the Data Module from the CrazyGames SDK** for progress save in the submission form. The game runs normally when the SDK is unavailable or ads are not filled.

The game has an English interface and adapts to desktop and mobile sizes, including the small 907 × 510 desktop frame. The English portal description and controls are in `marketing/listing.md`. Review the game's name for trademark conflicts and playtest the balance with other players. CrazyGames decides whether a submission is accepted.

Listing artwork is in `marketing/`: landscape (1920 × 1080), portrait (800 × 1200), and square (800 × 800) PNG covers, plus silent 15-second landscape (1920 × 1080) and portrait (1080 × 1620) MP4 previews. Upload these separately from the game ZIP. The previews are animated illustrations of the game's mechanics; capture live gameplay as well if the portal asks for footage. A draft English description and instructions are in `marketing/listing.md`.

## Files

- `index.html` — gameplay, vector parcel art, sound effects, and SDK integration
- `styles.css` — responsive interface and animations
- `docs/` — screenshots of the original prototype, kept for reference
- `marketing/` — cover images, preview videos, and the scripts used to create them

All rights reserved by the repository owner.
