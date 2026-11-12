# X-ZONE ambassador posts

Made with the `brand-ambassador-posts` skill (`.claude/skills/brand-ambassador-posts/SKILL.md`): paste an ambassador's Q&A and photos, and it writes the blog post, Instagram carousel and Facebook post, then builds the mock-up.

- `content/NN-slug.json` one file per ambassador (answers, social copy, edits, flags)
- `photos/` cropped ambassador photos and logo copies
- `template.html` + `build.py` build `xzone-ambassador-posts.html` (run `python3 ambassadors/build.py`)
- `notion_page.py` prints the Notion page body for an ambassador's Output Log row
- `export_instagram.py` exports each carousel slide to `instagram/<slug>-slide-<n>.png` at 1080 x 1350, ready to post

Live mock-up: https://claude.ai/artifact/4Mth5ByJpS4nTdkWobnJxA

| No. | Ambassador | Status |
|---|---|---|
| 15 | Jasmine Marsters, NZ Strongman | Draft, photos in |
| 14 | Mollie Allison, NZ beach volleyball | Draft, photos in |

## Buffer drafts (12 Nov, not scheduled)

| Ambassador | Instagram (xzonenz) | Facebook (XZone NZ) |
|---|---|---|
| Jasmine Marsters | `6af5a91a09e869a662dd3656` | `6af5af429b3fbcc1bc2fd62d` |
| Mollie Allison | `6af5a922a3fba876f6bfa072` | `6af5af478810c41b3dd1dc1f` |

Images load from the repo at commit ed4eb7f, so keep those files.

## Notion

Notion skill page: https://app.notion.com/p/416952099f258111812fcac79fe47560 (Head of Marketing > Skills)

Logged in Head of Marketing > Outputs > Output Log (`notion_page.py` makes each row's page):
- Jasmine: https://app.notion.com/p/416952099f2581e7a8dfc95f0d43d260
- Mollie: https://app.notion.com/p/416952099f25816fbcf3ea5fcea961b3
