# X-ZONE emails for Shopify (custom-coded)

Thirteen ready-to-paste emails for Shopify Messaging (Shopify Email), built from the designs on the canvas (Emails page). Each file is a complete custom-coded email: email-safe tables, inline styles, 600px wide, about 10 KB (Shopify allows 500 KB; Gmail clips above roughly 100 KB).

## Set up once

1. **Upload the images.** In Shopify admin go to **Content > Files** and upload everything in `images/` (the logo and the 13 hero photos). Keep the file names.
2. **Copy your Files folder address.** Copy the link of any uploaded image. Delete the file name and anything after it (including `?v=...`), so it ends in `/files/`. It looks like `https://cdn.shopify.com/s/files/1/0000/0000/0000/files/`.

## For each email

1. On a desktop, go to **Marketing > Create campaign > Shopify Email**, and choose to code your own email (custom-coded email).
2. Open the email's `.html` file in a text editor, copy all of it, and paste it into Shopify's code editor.
3. Near the top, replace `PASTE-SHOPIFY-FILES-FOLDER-URL-HERE/` with your Files folder address from step 2 above. Keep the slash at the end. Every image picks it up from that one line.
4. Replace every `[placeholder]` in square brackets (listed below), and the button links. The buttons point to `https://www.xzone.nz/` for now; swap in the right page with UTM tags.
5. Enter the **subject line** and **preview text** in Shopify's fields (listed below). The preview text is also hidden in the email itself.
6. Send a test to yourself and check it in Gmail, Outlook and on a phone before scheduling.

**Shopify variables already in each file:** `{{ unsubscribe_link }}` in the footer (required), and `{{ open_tracking_block }}` at the end for open tracking. Shopify's help pages name the tracking variable two ways; if the editor rejects `open_tracking_block`, change it to `open_tracking`.

**Fonts:** headlines use Poppins and fall back to Arial in email apps that block web fonts (for example Outlook on Windows). Body text is Arial, the brand's email font.

## The 13 emails

### Week 1: Price hold and summer kit (campaign, Thu 2026-11-26)
- File: `xzone-email-w01.html` with `images/xzone-email-w01-hero.jpg`
- Subject: Our old prices, held until [date]
- Preview text: Our prices went up this month. We are holding the old ones for now. Plus a summer kit list.
- Button: Shop at the old prices (point it to the right page with UTM tags)
- Placeholders to fill: [date], plus [business address] in the footer
- Open checks: 7 items in the calendar for this email

### Week 2: Gift guide and bruise colours (newsletter, Thu 2026-12-03)
- File: `xzone-email-w02.html` with `images/xzone-email-w02-hero.jpg`
- Subject: Christmas gifts, sorted by person
- Preview text: Gift ideas for the tradie, the tramper and the gardener. Plus what bruise colours mean.
- Button: Shop the gift guide (point it to the right page with UTM tags)
- Placeholders to fill: [date], plus [business address] in the footer
- Open checks: 9 items in the calendar for this email

### Week 3: Last Christmas order dates (newsletter, Thu 2026-12-10)
- File: `xzone-email-w03.html` with `images/xzone-email-w03-hero.jpg`
- Subject: Last order dates for Christmas
- Preview text: Order by [date urban] for urban delivery. Plus what goes wrong on day two of a tramp.
- Button: Order in time (point it to the right page with UTM tags)
- Placeholders to fill: [date], [date intl], [date rural], [date urban], [dispatch time], plus [business address] in the footer
- Open checks: 10 items in the calendar for this email

### Week 4: Pre-Christmas sale (campaign, Fri 2026-12-18)
- File: `xzone-email-w04.html` with `images/xzone-email-w04-hero.jpg`
- Subject: Our pre-Christmas sale is on
- Preview text: [offer]. Plus what to leave in the bach cupboard all summer.
- Button: Shop the sale (point it to the right page with UTM tags)
- Placeholders to fill: [date urban], [offer], plus [business address] in the footer
- Open checks: 6 items in the calendar for this email

### Week 5: Christmas greeting and Boxing Day (newsletter, Thu 2026-12-24)
- File: `xzone-email-w05.html` with `images/xzone-email-w05-hero.jpg`
- Subject: Meri Kirihimete from Jess and Dan
- Preview text: A thank you from us, a 20-second warm-up for backyard cricket and a Boxing Day recovery guide.
- Button: Read the recovery guide (point it to the right page with UTM tags)
- Placeholders to fill: [dispatch restart], plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 6: Joints Rub and stiff joints (campaign, Sun 2027-01-03)
- File: `xzone-email-w06.html` with `images/xzone-email-w06-hero.jpg`
- Subject: Stiff joints this summer: what helps
- Preview text: Why joints stiffen, three habits that help, and what independent lab tests found about our Joints Rub.
- Button: Meet the Joints Rub (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 6 items in the calendar for this email

### Week 7: DOMS and the lab results (newsletter, Thu 2027-01-07)
- File: `xzone-email-w07.html` with `images/xzone-email-w07-hero.jpg`
- Subject: Why day two hurts more than day one
- Preview text: DOMS explained, plus what independent lab tests found when they tested our three rubs.
- Button: Read the lab results (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 8: Heat or ice, answered (newsletter, Thu 2027-01-14)
- File: `xzone-email-w08.html` with `images/xzone-email-w08-hero.jpg`
- Subject: Heat or ice? It depends how new it is
- Preview text: The question we get asked most, answered. Plus a tip for shoulders after overhead work.
- Button: Meet the Joints Rub (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 9: Tennis elbow and site backs (newsletter, Thu 2027-01-21)
- File: `xzone-email-w09.html` with `images/xzone-email-w09-hero.jpg`
- Subject: Tennis elbow isn't just tennis
- Preview text: Why most people with it never held a racquet, and five free habits for your back.
- Button: Meet the Sports Rub (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 6 items in the calendar for this email

### Week 10: Sleep and medicine aches (newsletter, Thu 2027-01-28)
- File: `xzone-email-w10.html` with `images/xzone-email-w10-hero.jpg`
- Subject: Sleep is recovery
- Preview text: Three free sleep habits, and which common medicines can be linked to muscle aches.
- Button: Find your roll-on (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 11: Sports Rub: warm-up and recovery (campaign, Thu 2027-02-04)
- File: `xzone-email-w11.html` with `images/xzone-email-w11-hero.jpg`
- Subject: Warm up, then recover: the long-weekend version
- Preview text: First aid for the first 48 hours, a five-minute warm-up, and what independent lab tests found about our Sports Rub.
- Button: Meet the Sports Rub (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 12: The sideline kit for parents (newsletter, Thu 2027-02-11)
- File: `xzone-email-w12.html` with `images/xzone-email-w12-hero.jpg`
- Subject: Saturday sport is back
- Preview text: What to pack in the sideline bag, and when a knock means sit them out.
- Button: Meet the Relief range (point it to the right page with UTM tags)
- Placeholders to fill: none, plus [business address] in the footer
- Open checks: 8 items in the calendar for this email

### Week 13: Summer thank-you and survey (newsletter, Thu 2027-02-18)
- File: `xzone-email-w13.html` with `images/xzone-email-w13-hero.jpg`
- Subject: Thank you, and what should we cover next?
- Preview text: Thirteen weeks of lessons, your most-asked questions, and a two-minute survey for autumn.
- Button: Take the two-minute survey (point it to the right page with UTM tags)
- Placeholders to fill: [survey link], plus [business address] in the footer
- Open checks: 7 items in the calendar for this email

## Before the first send
- Fill in the business address in the footer of each file.
- Twelve of the 13 emails carry a full Judge.me review, word for word. Week 9 still uses Ben M's shortened quote until his full review is found (see `brief/reviews.md`).
- The hero photos for the new images are stand-ins waiting on client approval.
