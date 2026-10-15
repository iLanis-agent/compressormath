# Compressor Math

The air compressor honesty tool. The CFM on the box was measured at 40
PSI, where no tool lives. Compressor Math deflates the sticker to 90
PSI, counts the tank's free air between cut-in and cut-out, and holds
the tool's demand against the pump's honest flow.

- Live app: https://ilanis-agent.github.io/compressormath/app.html
- Landing: https://ilanis-agent.github.io/compressormath/

## What it does

1. **The CFM truth** - honest 90-PSI flow runs about 0.8x the 40-PSI
   sticker (labeled norm).
2. **The recovery truth** - tank gallons x (cut-out - cut-in) / 14.7 /
   7.48 cubic feet of free air, divided by the honest CFM into seconds.
3. **The duty truth** - tool demand as a percent of honest pump flow,
   with verdicts at 50, 80 and 100 percent.

## Files

- `engine.js` - pure functions (`cfmPlan`, `recoveryPlan`, `dutyPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 30 oracle cases, `node test.js` runs green

The derate is a labeled norm; the sander keeps the honest ledger.
