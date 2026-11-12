---
name: brand-ambassador-posts
description: Brand Ambassador Posts. Turns an X-ZONE ambassador's Q&A answers (the "Introducing; <Name>, <Sport>" blog series) and their photos into a finished blog post, an Instagram carousel and a Facebook post, then builds a visual mock-up of all three. Use when the user pastes an ambassador Q&A, says "ambassador post", "introducing <name>", or asks to mock up or redo an ambassador blog.
---

# Brand Ambassador Posts

X-ZONE runs a numbered blog series, "Introducing: <Name>, <Sport>", where Kiwi athletes and everyday people answer four set questions. This skill turns one ambassador's raw answers and photos into:

1. **Blog post** for xzone.nz (proofread, in their voice).
2. **Instagram carousel**, 3 slides: photo-led cover, quote card, second photo with "read the full story".
3. **Facebook post**: same story, shorter caption, link to the blog.
4. **Flags**: everything to confirm before it goes live.
5. **Mock-up page** showing all of it, built by `ambassadors/build.py`.

Read `brief/06-brand-spec.md` first. It wins over anything here.

## Inputs

- The pasted Q&A (often with the series boilerplate, a date and a "Find out more" link).
- Photos: collages are common. Crop each photo out on its own (find the divider bar, crop either side) and save to `ambassadors/photos/<slug>-1.jpg`, `-2.jpg`. Never crop out or cover the ambassador's face; never put our text over someone else's graphic (for example a federation's own title card).
- If a photo the user attached is not on disk, say so, set `"file": null` for it and keep going. The mock-up draws a labelled placeholder.

## Step 1: Edit the answers

The words are the ambassador's, not ours. Proofread, don't rewrite.

- Fix spelling, apostrophes and capitals (`kid's` → `kids`, `alot` → `a lot`, `apart of` → `a part of`, `i` → `I`, `STRONGMAN` → `strongman`). NZ spelling. Units with a space: `75 kg`.
- Move an answer to the question it belongs to (pros and cons often land under question 3; they belong in question 2).
- Keep first person, their phrasing, their claims about how they felt. Keep tense: if they wrote "will help", do not change it to "helps" (it changes the meaning; flag it instead).
- Do not add facts. If something is unclear (an acronym, a squad name, which product), keep their words and add a flag.
- Fix the series boilerplate every time: `Introducing; ` → `Introducing: `, `Kiwi's` → `Kiwis`, `in-between` → `in between`.

The four series questions (use this wording):

1. Who are you? Your background, occupation and where you are based.
2. What is your sport or passion, what drew you to it, and what are the pros and cons?
3. What is your biggest achievement to date, and what is your ultimate goal?
4. How does X-ZONE help?

## Step 2: Write the social posts

Brand voice rules (from the spec, non-negotiable):

- We voice for X-ZONE's own words; quotes stay in the ambassador's voice.
- **No emoji. No exclamation marks in headlines.** Sentence case.
- Never "cures", "proven", "clinically proven". Use "helps", "supports". Lab results only as "in independent lab tests", and ambassador posts normally don't need them.
- Never name a competitor.
- Pick the range from what they use. The product in the photo decides it (Sports Rub = Sports range). If unknown, `"range": "sports"` for athletes and a flag.

Instagram:
- **Cover** (`ig.headline` max 8 words, `ig.subline` max 9 words): lead with the most human or most striking fact in their answers (a number, a turning point), not "Meet our ambassador". Subline names them: "Ambassador 15: Jasmine Marsters, NZ Strongman".
- **Quote slide** (`ig.quote`): their best line about X-ZONE or their sport, verbatim from the edited answer, max about 30 words.
- **Caption** 80 to 160 words. First line is the lesson or hook from their story. Then who they are, the story, their advice. X-ZONE last, in their words. End "Read Jasmine's full story, link in bio." Max 5 hashtags, `#XZoneNZ #Aotearoa` first, then the sport.

Facebook: 40 to 90 words, first line the hook, link placeholder `{BLOG LINK}`, 0 to 2 hashtags.

## Step 3: Flags

Always include, adjusted to the person:
- Signed permission from the ambassador to use their name, words and photos on the blog and social.
- Photo credit for event photos (photographer or the event). Don't post someone's photo without it.
- Any wording change that could change meaning (tense, merged answers).
- Unclear terms, product and range, links you could not confirm.
- Publish date if the given date is in the past or clashes with the content calendar (`calendar/selection.json`).
- Tag handles (ambassador, event, federation) to confirm.

## Step 4: Save and build

Write `ambassadors/content/<NN>-<slug>.json` (NN = series number, two digits) in this shape:

```json
{
  "number": 15,
  "slug": "jasmine-marsters",
  "name": "Jasmine Marsters",
  "role": "NZ Strongman competitor",
  "sport": "NZ Strongman",
  "date": "2026-06-11",
  "range": "sports",
  "photos": [{"file": "jasmine-marsters-1.jpg", "alt": "...", "note": "what the photo shows"}],
  "answers": [{"q": 1, "paras": ["..."]}, {"q": 2, "paras": ["..."]}, {"q": 3, "paras": ["..."]}, {"q": 4, "paras": ["..."]}],
  "pull_quote": "line from their answers used mid-article",
  "more": {"label": "Find out more about NZ Strongman", "url": "https://..."},
  "ig": {"headline": "...", "subline": "...", "pill": "Sports range", "quote": "...", "caption": "...", "hashtags": "#XZoneNZ #Aotearoa ..."},
  "fb": {"caption": "..."},
  "edits": ["what we changed from their draft and why, one line each"],
  "flags": ["..."]
}
```

Optional `ig.cover_photo` and `ig.end_photo` (photo index, default 0 and 1) pick which photo goes on the carousel cover and last slide. The cover photo area is landscape, so a wide shot suits it; a tall action shot suits the last slide.

`range` is one of `relief`, `joints`, `sports`; it sets the pill text only. **Ambassador posts always use black + red** (black quote slide, red pill) whatever the range, on top of the usual green title band and lime subline. Black + red is reserved for the ambassador series: every other post follows the Instagram Posts rule of no red or orange (decided 12 Nov). The build handles it.

Then run:

```bash
python3 ambassadors/build.py
```

Then export the Instagram slides as ready-to-post 1080 x 1350 PNGs (into `ambassadors/instagram/<slug>-slide-<n>.png`):

```bash
python3 ambassadors/export_instagram.py
```

`build.py` reads every file in `ambassadors/content/`, newest number first, and writes `ambassadors/xzone-ambassador-posts.html` (photos and logo embedded). Publish that file as an Artifact. If `ambassadors/README.md` lists a live URL, update that artifact in place instead of making a new one, and record the URL there on first publish.

## Step 5 (only when asked): Buffer drafts

When the user asks to add posts to Buffer, save them as **drafts** (`saveToDraft: true`, `schedulingType: automatic`), never scheduled or published. Organisation "My organization"; get channel IDs from `list_channels` (Instagram `xzonenz`, Facebook page `XZone NZ`).

- Commit and push the images first, then point Buffer at raw GitHub URLs pinned to that commit: `https://raw.githubusercontent.com/Xzone-NZ/xzone/<commit sha>/ambassadors/...`. The repo is public, so these load. Don't delete those files while drafts use them.
- **Instagram:** `metadata.instagram = {type: "post", shouldShareToFeed: true}`, all three slides (`instagram/<slug>-slide-<n>.png`) as image assets with alt text, text = `ig.caption` + blank line + `ig.hashtags`.
- **Facebook:** `metadata.facebook = {type: "post"}`, the ambassador's main photo (`photos/<slug>-1.jpg`) as the image with alt text, text = `fb.caption` exactly (it keeps `{BLOG LINK}` until the blog is live).
- Save the returned IDs in the content JSON as `"buffer": {"instagram": "<id>", "facebook": "<id>"}` and in `ambassadors/README.md`.

## Step 6: Notion

The same skill lives in Notion as a skill page (Head of Marketing > Skills > Brand Ambassador Posts, https://app.notion.com/p/416952099f258111812fcac79fe47560). If you change the steps here, update that page to match.

Every finished ambassador goes into Notion (Head of Marketing > Outputs > **Output Log** database, data source `collection://2d89e36d-bbb6-4aad-8afd-3854cff4ebc6`). Fetch the data source first to confirm the schema, and search it for the ambassador's name so you update an existing row instead of adding a duplicate.

1. Generate the page body (flags as a checklist, the three IG slides as images, IG caption, FB post, full blog post, Buffer draft IDs, edits):

   ```bash
   python3 ambassadors/notion_page.py <slug> <commit sha the images were pushed in>
   ```

2. Create one row per ambassador with that output as `content` and these properties:

   | Property | Value |
   |---|---|
   | Output | `Ambassador <NN>: <Name>, <sport> (blog, IG carousel, FB post)` |
   | Status | `Awaiting approval` (they go to Jess and Dan) |
   | Skill | `Brand Ambassador Posts` |
   | Channel | `["Instagram", "Facebook"]` |
   | Format | `Carousel` |
   | Range | the range, e.g. `["Sports"]` |
   | Claims Check | `Ask Jess and Dan` while there are flags, `Pass` once cleared |
   | Design link | the mock-up artifact URL |
   | Flags | the flags, shortened to one line each |

   Leave Publish date empty until a date is agreed.
3. Add one line to the top of the **Activity Log** page table (newest first): date, what was done, `Awaiting approval by Jess and Dan`, link to the mock-up.

## Step 7: Report back

Send the user the exported slide PNGs for the new ambassador (SendUserFile), then give them the Notion row links, the IG headline and caption, the FB caption, the list of edits and the flags. Keep it short; the mock-up holds the rest.
