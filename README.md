# gta6-meme-x

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Dandidcee/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Dandidcee/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for the make.fun bounty [gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01):
post a GTA 6 meme on X.

## The meme

A Vice City sunset. A skeleton has been waiting on a park bench for GTA 6 since
2013, phone in hand. The make.fun ghost floats beside it with its magenta coin,
because the agent did not wait around: it entered a bounty and got paid.

Caption: *13 YEARS WAITING FOR GTA 6 — MY AI AGENT ALREADY GOT PAID — make.fun*.

The scene is drawn in code (`meme/make_meme.py`, Pillow): gradient sky, striped
sun, palms, bench and skeleton are shapes; the ghost is cut out of make.fun's
press badge `mark-1024.png` and composited into the scene.

```
python3 meme/make_meme.py     # -> meme/meme.png (1080x1080)
```

## What it does

`main.ts` copies `POST.json` to the output directory
(`$MAKEFUN_OUTPUT_DIR`, `/output` by default). `POST.json` holds the address of
the post on X.

## License

MIT
