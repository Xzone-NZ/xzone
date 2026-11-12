# X-ZONE ambassador posts

Made with the `brand-ambassador-posts` skill (`.claude/skills/brand-ambassador-posts/SKILL.md`): paste an ambassador's Q&A and photos, and it writes the blog post, Instagram carousel and Facebook post, then builds the mock-up.

- `content/NN-slug.json` one file per ambassador (answers, social copy, edits, flags)
- `photos/` cropped ambassador photos and logo copies
- `template.html` + `build.py` build `xzone-ambassador-posts.html` (run `python3 ambassadors/build.py`)
- `export_instagram.py` exports each carousel slide to `instagram/<slug>-slide-<n>.png` at 1080 x 1350, ready to post

Live mock-up: https://claude.ai/artifact/4Mth5ByJpS4nTdkWobnJxA

| No. | Ambassador | Status |
|---|---|---|
| 15 | Jasmine Marsters, NZ Strongman | Draft, photos in |
| 14 | Mollie Allison, NZ beach volleyball | Draft, photos in |

## Buffer
Instagram carousels saved as drafts on the xzonenz channel (12 Nov): Jasmine `6af5a91a09e869a662dd3656`, Mollie `6af5a922a3fba876f6bfa072`. Images load from the repo at commit ed4eb7f, so keep those files.
