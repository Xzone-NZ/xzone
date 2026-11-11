# Content-writing brief: X-ZONE summer social calendar

You are writing the finished content for every scheduled piece in a block of weeks of X-ZONE's 13-week Instagram + Facebook plan (23 Nov 2026 to 21 Feb 2027). X-ZONE is a NZ (Auckland) natural pain-relief brand: herbal rubs, sprays and roll-ons built on 11 native NZ healing herbs. Founders Jess Martin and Dan Holt (always "Jess and Dan", never "Danny").

## Read first (all paths absolute)
- Schedule (source of truth for which pieces exist): /tmp/claude-0/-home-user-xzone/1c2b980c-8918-5166-8845-76610c556195/scratchpad/cal/schedule.json — one object per week, `posts` rows (day, where, format, hook, blog, pillar, kind) and a `stories` line.
- Full plan text (strategy, pillars, lab results, stockists, wording rules, ambassadors): /root/.claude/projects/-home-user-xzone/1c2b980c-8918-5166-8845-76610c556195/tool-results/b8b99u8w2.txt
- Client brief: /home/user/xzone/brief/01-website-form.md
- Brand spec (voice rules win over everything): /home/user/xzone/brief/06-brand-spec.md

## Voice rules (non-negotiable)
- Write as "we". NZ English spelling. Plain, warm, short sentences. Kiwi, not corporate. Te reo greetings welcome (Kia ora, Ngā mihi, Aotearoa) with correct macrons.
- Personality: authentic, trustworthy, empowering, informative, generous.
- NO emoji anywhere. No exclamation marks in headlines. Humour rarely, never political or sexual.
- Never name a competitor (no Deep Heat, Voltaren, Tiger Balm, Om Rub etc., not even lowercase). A general contrast with pharmaceutical options is fine.
- Claims: "supports", "helps", "traditionally used". Never "cures", never "proven to reduce your pain", never "clinically proven". Lab results are in-vitro only: say "in independent lab tests (Trinity Bioactives), the Sports Rub reduced inflammation-associated cells by 54%" style, and never say a herb or product works like, or close to, a drug. Only use lab numbers that appear in the plan text.
- Health safety: include "see your GP" style guidance where an injury could be serious.
- Teach first: caption first line is the lesson. Product mention last. Promo pieces open with the lesson and close with the offer.
- Hashtags: max 5 on Instagram pieces, Aotearoa and herb names before generic pain tags. Facebook-only pieces: 0 to 2 hashtags.
- Do not invent facts. Anything you are not sure of (which range a herb is in, ambassador permission, label age guidance, offer details, prices, product bundles, subscription, stockist names) goes in `flags` and uses a {PLACEHOLDER} in the copy, e.g. {OFFER}, {CODE}, {LINK}, {DATE}. Known: trial pots from $3; 200+ stockists; 11 herbs; 11 to 14 active ingredients per jar where most rubs use 5 or 6.
- Audience note: core customer is 40 to 85 with chronic or higher pain (arthritis, sciatica, old sports injuries), active and outdoorsy. Joints Rub and Sports Rub are the flagships. Where a hook allows, speak to that person, not only young athletes.

## Client dates
- Price rise mid Nov, but prices are held at the old price for a month (shows as a discount to new customers): weeks 1 to 3 can say "old prices until {DATE}".
- Pre-Christmas sale from mid Dec (week 4). Their best ever sale was a one-day Buy 2 Get 1 Free with 3 emails beforehand.

## Output
Write ONE JSON file (UTF-8, valid JSON, no comments) at the path given in your task: an object `{"weeks":[...]}`. Each week:

```
{
 "week": 1,
 "theme": "...", "dates": "...",
 "posts": [ POST, ... ],      // exactly the rows in schedule.json for that week, same order
 "stories": [ STORY, ... ]    // one per item in that week's stories line (split on " · "), plus any it implies
}
```

POST:
```
{
 "id": "w1-mon",               // w{week}-{day lower}; if a day repeats (week 5 Sat), add -2
 "date": "2026-11-23",          // real date (Week 1 Mon = 2026-11-23, consecutive)
 "day": "Mon", "where": "IG + FB", "format": "Carousel", "pillar": "...", "kind": "Educate|Promo",
 "template": "ground|band|carousel|reel|fb|live|quote",
 "range": "relief|joints|sports|all|none",
 "photo": "bush|range|founders|bruise|shoulder|ankle",   // best match from the only six photos we have
 "title": "Short calendar title, 3 to 7 words",
 "about": "One sentence: what this piece is and why it is in the plan",
 "headline": "On-image headline, max 8 words, sentence case",
 "subline": "On-image subline, max 9 words",
 "pill": "Range pill text e.g. 'Sports range' or 'Herb 1 of 11' (optional)",
 "steps": [{"b":"bold label","t":"max 14 words"}],   // 0 to 3, for ground/band posts that teach steps
 "slides": [{"h":"slide headline","b":"slide body, max 30 words"}],   // carousel only: 5 to 7 slides, slide 1 is the cover
 "shots": [{"t":"0:00-0:04","shot":"what the camera sees","text":"on-screen words or ''"}],   // reel only: 4 to 8 shots, filmic, no voiceover unless Jess or Dan
 "duration": "20s",              // reel only
 "poll": ["option","option"],    // fb community polls only (optional)
 "caption": "Full ready-to-post caption, line breaks as \n. 60 to 160 words for IG, FB can be shorter",
 "hashtags": "#XZoneNZ #Aotearoa ...",
 "cta": "Save this | Link in bio | Comment below | Vote ...",
 "shoot": "The real photo or footage to capture for this piece (one sentence)",
 "flags": ["things to confirm with the client before posting"]
}
```
Template guide: carousel → "carousel"; Reel → "reel"; FB community post → "fb"; Facebook Live → "live"; a customer or ambassador quote post → "quote"; single posts that teach in steps → "band"; other single posts → "ground".

STORY:
```
{"id":"w1-s1","day":"Mon","type":"quiz|question|poll|countdown|link|bts|testimonial|prompt|explainer|recap|greeting",
 "text":"the words on the story frame, max 20 words",
 "options":["A","B"],            // quiz/poll only
 "note":"how to run it, one line"}
```

When done, validate with: `python3 -c "import json;d=json.load(open(PATH));print(sum(len(w['posts']) for w in d['weeks']))"` and make sure the count equals the rows for your weeks. Reply with only the file path, the post count, and the full list of flags (deduplicated).
