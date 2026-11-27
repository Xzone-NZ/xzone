# X-ZONE Social Builder: visuals pipeline

Renders the on-brand images and reels for posts drafted in the Social Builder app (a private claude.ai artifact).

```
node social-builder/render.js social-builder/specs/<id>.json [outDir]
```

Run from the repo root. Needs Node with Playwright (Chromium) and ffmpeg. Fonts come from `guides/fonts` (Poppins), the logo from `tools/logo-white.png`, photos from `brief/photos`.

| Format | Output |
| --- | --- |
| post | `post.png` 1080x1350 |
| carousel | `slide-1.png` ... 1080x1350, 2 to 8 slides, logo on every slide, SWIPE cue on slide 1 |
| reel | `beat-N.png`, `cover.png` and a silent `reel.mp4`, all 1080x1920 |

Every render also writes `preview-*.jpg` (600 px) and, for reels, `preview-reel.mp4` (540x960) for the app.

## Spec format

```json
{ "id": "kebab-id", "format": "post",
  "slides": [ { "photo": "brief/photos/kumarahou.jpg", "hook": "Eleven native herbs. [[One]] rub.",
                "sub": "Plain supporting line.", "callout": null, "bullets": [], "button": null } ] }
```

Reels use `"beats": [{ "photo", "hook", "sub", "seconds" }]` instead of `slides`.

- `[[word]]` puts the lime underline behind one key word. One per slide. Never a highlighter block, never lime text.
- `**word**` is bold.
- Hook: at most two lines. The renderer fails if text runs into the logo, a hook runs to three lines, or an em or en dash appears.
- Look and rules: `brief/06-brand-spec.md`, "Final look".

## Publishing rule (used by the scheduled task "Social Builder visuals")

New files only, under `social-builder/media/<id>/`, on a branch named `social-visuals/<id>` and a pull request into `main`. Never replace, move or delete an existing file. Never merge. Buffer only ever receives raw.githubusercontent.com URLs from `main`, after the approver has merged.

`specs/test-*.json` are layout tests with illustrative copy. They are not posts.
