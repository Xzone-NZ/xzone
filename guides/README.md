# Team guides

Branded A4 PDFs for the X-ZONE marketing team.

| PDF | What it covers |
|---|---|
| `xzone-guide-prompting-the-marketing-project.pdf` | How to prompt the Marketing Project in Claude: the five-part prompt, copy-ready prompts for every content type (weekly set, posts, carousels, Reels, stories, Facebook, newsletters, sale emails, HTML emails, testimonials, ambassadors, blogs, stockists, reports), feedback and sign-off, quick reference. |
| `xzone-guide-ideas-and-weekly-review.pdf` | The Notion Ideas database: how to add ideas, the status flow, what the weekly scheduled review reports, who does what, how to act on it, summer moments to watch, and a reference prompt for the scheduled task. |

## Editing

The words are in `guide_content.py`, the styles in `style.css` (colours and Poppins from `brief/06-brand-spec.md`). Rebuild both PDFs with:

```bash
python3 guides/build.py
```

`build.py` writes the HTML, then `render.js` prints it with Playwright (Node) and warns if any page's content runs into the footer.
