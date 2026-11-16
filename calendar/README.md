# X-ZONE summer content calendar

13 weeks (23 Nov 2026 to 21 Feb 2027). Scheduled: 39 posts (3 a week, IG + FB), 13 emails (4 campaigns), 26 light stories. The content files hold 78 drafted posts; `selection.json` picks the 3 a week, the rest are an idea bank.

- `content-a.json` weeks 1 to 4, `content-b.json` weeks 5 to 8, `content-c.json` weeks 9 to 13: every post's on-image text, slides, Reel shot list, caption, hashtags, shoot note and items to confirm.
- `extra.json` the 13 emails, the week 3 testimonial graphic and the merged Boxing Day post.
- `selection.json` which posts are scheduled, and on which day.
- `schedule.json` the slot list pulled from the summer plan.
- `BRIEF.md` the writing rules the content follows.
- `template.html` + `build.py` build `xzone-summer-calendar.html` (run `python3 build.py`).
- `buffer_export.py` writes `buffer/buffer-posts.json` and `.csv`: the 39 scheduled posts as Buffer drafts (78 rows, Instagram and Facebook), 7pm NZT, caption plus hashtags, media and confirm notes. Re-run after any content change.
- **In Buffer (16 Nov 2026):** 82 drafts (41 posts on Instagram and Facebook), each set to its date at 7pm NZT. All 54 carousel, single-post and review drafts have their images from `buffer/media/`, pinned to commit caa314e so they can't change under Buffer. Still to do before scheduling: the 26 Reel drafts need their filmed video (the week 1 Tuesday and week 2 Saturday Reels carry an old auto-made slideshow video), the two ambassador Instagram drafts have no date yet (calendar: Jasmine Sat 9 Jan, Mollie Thu 28 Jan), and some captions and slides still hold {PLACEHOLDERS}. Drafts never publish on their own. The free plan holds only 10 scheduled posts at a time, so schedule a week or two ahead. Edits made in Buffer do not flow back here. If a design changes, re-run the export, commit, and re-attach that post's images pinned to the new commit.
- `export_media.py` makes the upload-ready files in `buffer/media/` (run `python3 build.py && python3 export_media.py && python3 buffer_export.py`): one folder per scheduled post, with carousels as `slide-01.jpg`... and single posts as `post.jpg` (1080 x 1350), Reels as `reel-cover.jpg` (1080 x 1920; the video itself is filmed from the shot list), and stories in `buffer/media/stories/` (1080 x 1920). `buffer/media-manifest.json` lists every file. `buffer-posts.csv` and `buffer-stories.csv` give each draft its files as raw GitHub URLs on the default branch, which Buffer can fetch. Five designs (`w4-s2`, `w6-s9`, `w10-s5`, `w12-fri`, `w13-s2`) use stock photos that live only on the design canvas, so their photo is the 540px preview scaled up: export those from the canvas before posting.
- `designs/` the 65 hand-built designs (posts, Reels and stories, weeks 1 to 13) rendered from the design canvas. `build.py` shows these in the calendar and feed in place of the generated previews; publish them alongside the pages as supporting files.
- `small/` stand-in photos used in the previews. Swap for real shoot photos later. cricket, aoraki, bushwalk, hands and handsclose were added 12 Nov and are not yet approved by the client.
- Preview style is the approved Round 2 social style (see `brief/06-brand-spec.md`, Social design direction).

Live page: https://claude.ai/artifact/MBFynFP4giMK47gpidW4rM
Feed mock-up (built by the same build.py from feed-template.html): https://claude.ai/artifact/6BxDXBEPrE5kgjmoraMDmu
