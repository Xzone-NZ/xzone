"""Words for the two X-ZONE team guides. Each page is a function that takes the
prompt() helper and returns HTML. Keep to the brand voice: NZ spelling, no emoji,
no exclamation marks in headlines."""

IDEAS_URL = "https://app.notion.com/p/777c8288fbaa42098e1708801aded374"
HUB_URL = "https://app.notion.com/p/416952099f2581b9a90ce335ec6b3295"


def type_block(title, skill, use, give, prompt_text, back, follow, P, extra=""):
    tags = "".join(f'<span class="tag skill">{s}</span>' for s in skill)
    fol = "".join(f"<li>{f}</li>" for f in follow)
    give_li = "".join(f"<li>{g}</li>" for g in give)
    return f'''
<div class="type-head"><div><h3 style="margin:0;font-size:13.5pt">{title}</h3>
<p class="small" style="margin:.5mm 0 0">{use}</p></div><div class="meta">{tags}</div></div>
<div class="grid2" style="grid-template-columns:1fr 1.55fr;gap:5mm">
  <div><h4 style="margin-top:0">Give it</h4><ul>{give_li}</ul>
       <h4>You get back</h4><p>{back}</p></div>
  <div>{P(prompt_text)}<h4 style="margin-top:0">Then try</h4><ul style="margin-bottom:0">{fol}</ul></div>
</div>{extra}'''


# ---------------------------------------------------------------- Guide 1
def g1_p2(P):
    return f'''
<div class="kicker">Start here</div>
<h2>How the Marketing Project <span class="hl">works</span></h2>
<p class="lede">The Marketing Project in Claude acts as X-ZONE's Head of Marketing. It already knows the brand, the
products, the claims rules and the summer calendar. Your job is to tell it <b>what</b> you want, <b>for which range</b>,
<b>when</b> it goes out and <b>what to work from</b>. It does the rest, as a draft for Jess and Dan.</p>

<h3>What happens every time you ask for content</h3>
<div class="flow">
  <div class="f"><b>1. Loads context</b>Reads the Role Card, Business Context and Caption Guide in Notion, plus the brand spec and calendar on GitHub.</div>
  <div class="f"><b>2. Picks a skill</b>Finds the matching playbook (Reels, Stories, Campaign Email...) and follows its steps.</div>
  <div class="f"><b>3. Checks Ideas</b>Looks in the Ideas database for shortlisted ideas that fit.</div>
  <div class="f"><b>4. Drafts</b>Writes the copy, shot list or email, then runs Claims Check.</div>
  <div class="f dark"><b>5. Logs it</b>Saves the piece to the Output Log as "Awaiting approval" for Jess and Dan.</div>
</div>

<h3>The five-part prompt</h3>
<p>Every good request has these five parts. Leave one out and the Project will either ask you or guess. A guess is slower than a sentence.</p>
<table>
<tr><th style="width:23%">Part</th><th style="width:37%">What to say</th><th>Example</th></tr>
<tr><td><b>1. The format</b></td><td>Reel, carousel, story, newsletter... Naming the skill is even better.</td><td>"Use the Reels skill to plan a Reel"</td></tr>
<tr><td><b>2. The range</b></td><td>Relief, Joints, Sports, or brand (all ranges).</td><td>"for Joints"</td></tr>
<tr><td><b>3. When</b></td><td>Calendar week or the go-live date.</td><td>"for week 3, Wednesday 9 Dec"</td></tr>
<tr><td><b>4. Work from</b></td><td>An idea from the Ideas database, a review, a photo, a customer question, notes.</td><td>"from the idea 'Hands that work hard'"</td></tr>
<tr><td><b>5. Anything special</b></td><td>Who is on camera, an offer Jess and Dan have set, a link, a deadline.</td><td>"Jess is on camera, filmed in the garden"</td></tr>
</table>
{P("""Use the [skill name] skill to create a [format] for [range], going out [week / date].
Work from [the idea, review, photo or notes].
[Anything special: who is on camera, the offer as Jess and Dan set it, the link to use].""", "The template")}
'''


def g1_p3(P):
    return f'''
<div class="kicker">Before you type</div>
<h2>Seven rules that <span class="hl">save time</span></h2>
<div class="grid2" style="margin-top:4mm">
<div>
<div class="step"><span class="num">1</span><div><b>One chat per job.</b> Start a new chat in the Marketing Project for each piece or weekly batch. Long chats get muddled and slow.</div></div>
<div class="step"><span class="num">2</span><div><b>Name the skill.</b> "Use the Stories skill" removes guesswork. The full list is on page 12.</div></div>
<div class="step"><span class="num">3</span><div><b>Paste the raw material.</b> Paste the review word for word, attach the photo, copy the customer's question. The Project only quotes what it can see.</div></div>
<div class="step"><span class="num">4</span><div><b>Never ask it to invent an offer.</b> Sales, codes, bundles and free shipping come from Jess and Dan only. Give the exact wording or it will stop and ask.</div></div>
</div>
<div>
<div class="step"><span class="num">5</span><div><b>Point to an idea.</b> If the idea is in the Ideas database, give its title. The Project will link the finished piece back to it.</div></div>
<div class="step"><span class="num">6</span><div><b>Be specific with changes.</b> "Shorter, warmer opening, swap the photo for the knee shot" beats "make it better".</div></div>
<div class="step"><span class="num">7</span><div><b>Nothing goes out unapproved.</b> Everything is a draft until Jess and Dan approve it. Then it is scheduled in Meta Business Suite or built in Shopify Messaging.</div></div>
</div>
</div>

<div class="note green" style="margin-top:4mm"><b>The rules it always follows for you:</b> NZ spelling. No emoji. No exclamation marks in headlines. "Supports", "helps",
"traditionally used", never "cures" or "proven". Lab results are always "in independent lab tests". Name the herbs. Write as "we". 80% educate, 20% sell.
Headlines are hooks. You do not need to repeat these in your prompt.</div>

<h3>Where things live</h3>
<table>
<tr><th style="width:30%">What</th><th>Where</th></tr>
<tr><td>The Marketing Project</td><td>claude.ai, Projects, Marketing. Always start chats from inside the Project so it has its instructions and connectors.</td></tr>
<tr><td>Ideas database</td><td>Notion, Head of Marketing, Ideas. Drop every idea here (see the Ideas guide).</td></tr>
<tr><td>Finished drafts</td><td>Notion, Head of Marketing, Outputs, Output Log. One row per piece, with its status.</td></tr>
<tr><td>Skills (playbooks)</td><td>Notion, Head of Marketing, Skills.</td></tr>
<tr><td>Brand spec, photos, calendar</td><td>GitHub, Xzone-NZ/xzone: <code>brief/06-brand-spec.md</code>, <code>brief/photos/</code>, <code>calendar/</code>.</td></tr>
</table>

<h3>If the Project says a connector failed</h3>
<p>It will stop rather than work from memory. Check Notion and GitHub are switched on for the Project (the tools menu in the chat box), then ask again with "Try again now the connectors are on".</p>
'''


def g1_p4(P):
    a = type_block("Weekly social content set", ["Weekly Social Content Set"],
        "The week's three Facebook and Instagram posts, planned together and handed to the channel skills.",
        ["The calendar week", "Any idea titles you want used", "Range focus, if any", "Anything happening that week (event, sale set by Jess and Dan)"],
        """Use the Weekly Social Content Set skill to plan week [number] ([dates]).
Check the calendar first for anything already drafted. Pull from Shortlisted ideas in the Ideas database, and use [idea titles] if they fit.
Range focus: [Relief / Joints / Sports / mixed].
Give me the week plan, then draft each piece with its channel skill.""",
        "A week plan (which format on which day), then each post drafted in full: hook, design notes, caption, hashtags, Claims Check, one Output Log row each.",
        ["\"Swap Friday's post for a testimonial, using this review: [paste]\"",
         "\"Show me the three hooks side by side before you write the captions\""], P)
    b = type_block("Instagram single post", ["Instagram Posts"],
        "One feed image, 1080 x 1350, cross-posted to Facebook.",
        ["The topic or idea", "Range", "The photo you want (file name or attach it)", "Go-live date"],
        """Use the Instagram Posts skill to create a single post for [range] going out [date].
Topic: [what it is about, or the idea title].
Photo: [file name from brief/photos, or attached].
Give me the hook, the design layout to build in Canva, the caption and hashtags.""",
        "A hook headline with its highlight word, layout notes (Post A, B or C style), caption of 60 to 160 words, up to 5 hashtags, Claims Check result.",
        ["\"Give me three other hook options\"",
         "\"Make it white ground with navy text, it's a Joints post\""], P)
    return f'<div class="kicker">Social</div><h2>Weekly set and <span class="hl">single posts</span></h2>{a}<div class="divider"></div>{b}'


def g1_p5(P):
    a = type_block("Carousel", ["Instagram Posts"],
        "Multi-slide teaching posts: how-tos, herb guides, myth busters. Up to 7 slides.",
        ["The lesson you want to teach", "Range", "Number of slides (default 6 to 7)", "Photos for the cover"],
        """Use the Instagram Posts skill to create a [number]-slide carousel for [range], going out [date].
The lesson: [e.g. what to do in the first 48 hours after a rolled ankle].
Cover photo: [file name or attached].
Give me the cover hook, the words for each slide, the caption and the design notes.""",
        "Slide-by-slide text (cover hook, one idea per slide, a save/share last slide), design notes per slide, caption, hashtags, Claims Check.",
        ["\"Cut it to 5 slides and keep the strongest points\"",
         "\"Turn slide 3 into a simple numbered list\""], P)
    b = type_block("Reel", ["Reels"],
        "Top priority format: 4 a month, on Wednesdays. 15 to 30 seconds.",
        ["The type: how-to, herb of the week, founders, first aid moment", "Who is on camera (Jess, Dan, a customer)", "Where you will film", "Range and date"],
        """Use the Reels skill to plan a [type] Reel for [range], going out [date].
Topic: [what it shows].
On camera: [Jess / Dan / hands only / customer name]. Location: [where].
Give me the cover hook, a shot list with on-screen words, the caption and a shoot note.""",
        "Cover hook, subline and \"Watch...\" play line; a 4 to 8 shot list with time codes and on-screen text; end card; caption; shoot note with permissions to confirm.",
        ["\"We only have 10 minutes to film. Simplify the shot list to 4 shots on a phone\"",
         "\"Write Dan's voiceover script for this, in his words\""], P,
        '<div class="note lime" style="margin-top:3mm"><b>Filming tip:</b> the first 3 seconds must show the problem (the sore knee, the stiff hands). Natural light, real NZ places, no stock. Only Jess or Dan do voiceovers.</div>')
    return f'<div class="kicker">Social</div><h2>Carousels and <span class="hl">Reels</span></h2>{a}<div class="divider"></div>{b}'


def g1_p6(P):
    a = type_block("Stories", ["Stories"],
        "Polls, question boxes, quizzes and link stickers. Full photo plus a two-option poll and a \"tomorrow we share...\" line.",
        ["What you want to learn from followers, or what you are teasing", "Number of frames", "Photos", "Date"],
        """Use the Stories skill to make a [number]-frame story set for [date].
Goal: [e.g. find out which joint bothers people most, to plan next week's carousel].
Photos: [file names or attached].
Include a poll or question sticker and a "tomorrow we share..." line.""",
        "Each frame's words, sticker type and options, photo, and run notes (what to post the next day with the answers).",
        ["\"Turn the poll results into a carousel idea and add it to Ideas\"",
         "\"Make a 3-frame quiz on the native herbs in the Joints range\""], P)
    b = type_block("Facebook post, poll or Live", ["Facebook Posts"],
        "Community posts, Facebook-only polls and run sheets for a Facebook Live with Jess and Dan.",
        ["The type: cross-post, community post, poll or Live", "Topic", "For a Live: date, time, who hosts, length"],
        """Use the Facebook Posts skill to create a [community post / poll / Live run sheet] for [date].
Topic: [what it is about].
[For a Live: Jess and Dan host, [length] minutes, at [time]. Questions people have asked: [paste].]
Write it for our Facebook audience, which skews older than Instagram.""",
        "A Facebook caption (longer and chattier than Instagram), or poll options, or a Live run sheet with timings, talking points and safe answers to likely questions.",
        ["\"Turn this week's Instagram carousel into a Facebook post\"",
         "\"Add three questions we can expect and approved ways to answer them\""], P,
        '<div class="note" style="margin-top:3mm"><b>Health questions in comments or Lives:</b> the Project never answers "will this help my condition". It drafts a kind reply that points people to their GP or pharmacist, and flags it for Jess and Dan.</div>')
    return f'<div class="kicker">Social</div><h2>Stories and <span class="hl">Facebook</span></h2>{a}<div class="divider"></div>{b}'


def g1_p7(P):
    a = type_block("Weekly newsletter", ["Campaign Email Sequence"],
        "The weekly email to subscribers via Shopify Messaging: one lesson, one proof point, one product link.",
        ["The topic (a herb, a pain topic, a how-to)", "A review to quote, if you have one", "The product link", "Send date"],
        """Use the Campaign Email Sequence skill to write this week's newsletter, sending [date].
Topic: [the one lesson].
Proof point: [paste a Judge.me review word for word, with the name as shown].
Product link: [URL].
Give me two subject lines, preview text, the body and the button.""",
        "Subject line plus an alternative, preview text, short body, button text and link, suggested social posts to match, Claims Check.",
        ["\"Make the subject line a curiosity hook, under 45 characters\"",
         "\"Now build it as a designed email with the Shopify E-Newsletter skill\""], P)
    b = type_block("Sale campaign (3 emails)", ["Campaign Email Sequence"],
        "The build-up to a sale moment, modelled on Labour Day Buy 2 Get 1 Free: tease, reasons to believe, offer day.",
        ["The offer, word for word, as Jess and Dan set it", "Start and end dates and times", "Range focus", "Segment, if any"],
        """Use the Campaign Email Sequence skill to write the 3-email build-up for [campaign name].
Offer (set by Jess and Dan): [exact wording].
Runs: [start date and time] to [end date and time]. Range focus: [range].
Segment: [all subscribers / past Joints buyers / ...].
Also suggest the matching social posts and stories.""",
        "Email 1 (tease, 3 to 5 days out), Email 2 (customer story and the approved lab line, day before), Email 3 (offer day, one button), each with subjects and preview text, plus social support.",
        ["\"Write a last-chance email for the final 6 hours\"",
         "\"Give me story frames counting down to the sale\""], P,
        '<div class="note lime" style="margin-top:3mm"><b>No offer, no campaign.</b> If the offer is not confirmed in writing by Jess and Dan, the Project stops and asks. Offers so far: the old-price hold after the November price rise and the mid-December pre-Christmas sale.</div>')
    return f'<div class="kicker">Email</div><h2>Newsletters and <span class="hl">sale emails</span></h2>{a}<div class="divider"></div>{b}'


def g1_p8(P):
    a = type_block("Designed HTML email", ["Shopify E-Newsletter"],
        "Turns an approved email into a ready-to-paste, branded custom-coded email for Shopify Messaging.",
        ["The approved email (or its Output Log row)", "The hero photo", "Product links"],
        """Use the Shopify E-Newsletter skill to build the approved email "[email name]" as a designed HTML email.
Hero photo: [file name or attached].
Product links: [URLs].
Give me the code to paste into Shopify Messaging and a preview.""",
        "HTML in the X-ZONE layout (green header, lime highlights, Poppins/Arial), a preview to check, and notes on anything to test before sending.",
        ["\"Send me a test version with the product block moved above the review\"",
         "\"Check it on a narrow phone screen and fix anything that wraps badly\""], P)
    b = type_block("Testimonial graphic", ["Testimonial to Graphic"],
        "Turns a public review into a proof post. Reviews are quoted in full, word for word.",
        ["The review, pasted exactly as it appears", "The reviewer's name as shown", "Where it is from (Judge.me, Google) and the product"],
        """Use the Testimonial to Graphic skill to turn this review into a post for [date]:
"[paste the review exactly]"
[Name as shown], Verified review, [product], from [Judge.me / Google Reviews].
Give me the quote layout, caption and design brief.""",
        "Quote layout (photo on top, review in a band below), caption that lets the customer do the selling, design brief, Claims Check (a review can still contain a claim we cannot repeat).",
        ["\"Find our three best Joints reviews in the Ideas database and draft all three\"",
         "\"Make a story version of this review\""], P)
    return f'<div class="kicker">Email and proof</div><h2>Designed emails and <span class="hl">reviews</span></h2>{a}<div class="divider"></div>{b}'


def g1_p9(P):
    a = type_block("Brand ambassador post", ["Brand Ambassador Posts"],
        "The \"Introducing: Name, Sport\" series: blog post, 3-slide Instagram carousel and Facebook post.",
        ["The ambassador's Q&A answers, pasted in full", "Their photos (attach them)", "The publish date"],
        """Use the Brand Ambassador Posts skill. Here is [name]'s Q&A for the Introducing series, publishing [date]:
[paste their answers]
Photos attached. Give me the blog post, the carousel, the Facebook post and anything to check with them.""",
        "A proofread blog post in their own words, a 3-slide carousel (black and red ambassador style), a Facebook post, a mock-up and a list of flags to confirm with the ambassador.",
        ["\"Write a short message asking [name] to confirm the flagged points\"",
         "\"Pull one quote from the blog for a story\""], P)
    b = type_block("Blog post", ["No skill yet"],
        "Monthly blog for xzone.nz. There is no Blog skill yet, so the Project works from the Role Card and Business Context and will say so.",
        ["The topic and the search phrase people would type", "Rough length (800 to 1,200 words is typical)", "Products to link"],
        """There is no Blog skill yet, so use the Role Card, Business Context and Caption Guide.
Write a blog post for xzone.nz on [topic], aimed at people searching "[search phrase]".
About [length] words. Teach first, product last. Link to [products].
Give me a title, meta description, the post with subheadings, and 3 social posts to share it.
Then tell me whether this should become a skill.""",
        "Title, meta description, the post, social posts to promote it, Claims Check, and a suggestion on turning it into a skill.",
        ["\"Yes, draft a Blog skill from this and add it to the Skills page for Jess and Dan to approve\""], P)
    return f'<div class="kicker">Long form</div><h2>Ambassadors and <span class="hl">blogs</span></h2>{a}<div class="divider"></div>{b}'


def g1_p10(P):
    a = type_block("Stockist marketing pack", ["Stockist Marketing Pack"],
        "Support for the 200+ pharmacies, health stores and practitioners: email, leave-behind copy, shelf talkers.",
        ["Stockist type (pharmacy, health store, practitioner)", "What it is for (new stockist, seasonal push, launch)", "Range focus"],
        """Use the Stockist Marketing Pack skill to make a pack for [stockist type] for [purpose, e.g. summer sports injuries].
Range focus: [range].
Give me the stockist email, leave-behind copy and any in-store or social assets they could use.""",
        "Stockist email, leave-behind copy, suggested posts stockists can share, all through Claims Check. Pricing and orders stay with Sales.",
        ["\"Shorten the leave-behind to fit an A5 card\"",
         "\"Write a social post a stockist can share that tags them\""], P)
    b = type_block("Monthly marketing report", ["Monthly Marketing Report"],
        "First week of each month: revenue, ads, email and social results against the $40k and $80k targets.",
        ["The month", "Any numbers the Project cannot see: Shopify sales, Meta and Google ad results, email results (paste or attach exports)"],
        """Use the Monthly Marketing Report skill for [month].
Here are the numbers: [paste Shopify revenue, ad spend and results, email opens and revenue, or attach the exports].
Compare to target and last month, show what worked and what didn't, and recommend next month's focus.""",
        "A report page in Notion: headline numbers, what worked, what to stop, next month's plan, and ideas added to the Ideas database.",
        ["\"Which three posts drove the most saves and shares? Add similar ideas to Ideas\""], P)
    return f'<div class="kicker">Business</div><h2>Stockists and <span class="hl">reporting</span></h2>{a}<div class="divider"></div>{b}'


def g1_p11(P):
    return f'''
<div class="kicker">After the first draft</div>
<h2>Feedback, changes and <span class="hl">sign-off</span></h2>
<p class="lede">Most pieces need one round of changes. Say exactly what to change, and when Jess and Dan give feedback,
tell the Project so it learns the rule for next time.</p>
<div class="grid2">
<div>
<h3 style="margin-top:0">Asking for changes</h3>
{P("""Changes to [piece name]:
- Hook: [shorter / more curious / use the word "..."].
- Caption: [cut to under 100 words / warmer opening].
- Photo: swap to [file name].
Keep everything else the same and update the Output Log row.""", "Revise a draft")}
{P("""Give me [3] different options for the [hook / subject line / opening line], each a different angle.""", "Get options")}
<h3>Passing on Jess and Dan's feedback</h3>
{P("""Jess and Dan's feedback on [piece name]: "[paste their words]".
Apply it, set the Output Log status to [Approved / Changes needed], and if this should be a permanent rule, suggest where to add it (Role Card, the skill, or the Caption Guide).""", "Feedback")}
</div>
<div>
<h3 style="margin-top:0">Once it's approved</h3>
{P("""[Piece name] is approved and scheduled in Meta Business Suite for [date and time].
Set the Output Log row to Scheduled and mark the idea it came from as Planned.""", "Scheduled")}
{P("""[Piece name] went live on [date]. Results after [7] days: [reach, plays, saves, shares, comments / opens, clicks, orders].
Add these to the Output Log row, mark the idea as Used, and tell me what to repeat.""", "Results")}
<h3>Getting a batch ready for approval</h3>
{P("""List everything in the Output Log that is Awaiting approval, as one short message I can send to Jess and Dan, with the link to each piece.""", "Approval batch")}
</div>
</div>
'''


def g1_p12(P):
    rows = [
        ("Week's 3 Facebook + Instagram posts", "Weekly Social Content Set"),
        ("Single post or carousel (1080 x 1350)", "Instagram Posts"),
        ("Reel: hook, shot list, cover", "Reels"),
        ("Stories: polls, questions, quizzes", "Stories"),
        ("Facebook post, poll, Live", "Facebook Posts"),
        ("Weekly newsletter or sale emails", "Campaign Email Sequence"),
        ("Designed HTML email for Shopify", "Shopify E-Newsletter"),
        ("Review into a proof post", "Testimonial to Graphic"),
        ("Ambassador Q&A into blog + posts", "Brand Ambassador Posts"),
        ("Pharmacy, health store, practitioner support", "Stockist Marketing Pack"),
        ("Monthly results", "Monthly Marketing Report"),
        ("Every public-facing draft", "Claims Check (runs automatically)"),
    ]
    tr = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td></tr>" for a, b in rows)
    return f'''
<div class="kicker">Keep this handy</div>
<h2>Quick <span class="hl">reference</span></h2>
<div class="grid2" style="grid-template-columns:1.1fr 1fr">
<div>
<table><tr><th>I need...</th><th>Ask for the skill</th></tr>{tr}</table>
<p class="small">Skills grow over time. Ask "Which skills do you have?" for the current list.</p>
</div>
<div>
<h3 style="margin-top:0">When something goes wrong</h3>
<table>
<tr><th style="width:42%">It...</th><th>Do this</th></tr>
<tr><td>says a connector failed</td><td>Turn Notion and GitHub on in the chat's tools menu, then "Try again".</td></tr>
<tr><td>asks about an offer</td><td>Get the exact offer from Jess and Dan. It will not invent one.</td></tr>
<tr><td>flags an open question</td><td>It is in <code>brief/open-questions.md</code>. Ask Jess and Dan, then tell the Project the answer.</td></tr>
<tr><td>uses the wrong photo</td><td>Give the file name from <code>brief/photos</code>, or attach the photo.</td></tr>
<tr><td>sounds generic</td><td>Paste a real review, customer question or detail. Specifics make the copy.</td></tr>
<tr><td>repeats an old post</td><td>"Check the Output Log and calendar for anything similar first."</td></tr>
<tr><td>forgets to log it</td><td>"Write this back to the Output Log and Activity Log now."</td></tr>
</table>
<div class="note green"><b>Got an idea, not a request?</b> Drop it in the Ideas database instead. The weekly review will tell you if and when to make it, and who should. See the Ideas guide.</div>
</div>
</div>
'''


# ---------------------------------------------------------------- Guide 2
def g2_p2(P):
    return f'''
<div class="kicker">The loop</div>
<h2>From a thought to a <span class="hl">post</span></h2>
<p class="lede">Good content ideas turn up everywhere: a customer question at the market, a comment on a Reel, a review,
something you saw on a walk. The Ideas database catches them all, and once a week a scheduled review in Claude
reads them and tells the team what to make next, who should make it and in what format.</p>
<div class="flow">
  <div class="f"><b>1. Drop it</b>Anyone adds the idea to Notion, Head of Marketing, Ideas. Status starts as New.</div>
  <div class="f"><b>2. Weekly review</b>The scheduled task reads every New idea, checks the content plan and what's trending.</div>
  <div class="f"><b>3. Decide</b>The team reads the review and agrees what to shortlist, park or make now.</div>
  <div class="f"><b>4. Make it</b>Use the prompts in the Prompting guide. The idea moves to Planned.</div>
  <div class="f dark"><b>5. Used</b>Once live, the idea is marked Used and linked to the finished piece.</div>
</div>
<div class="grid2">
<div class="card"><h3>Where it lives</h3>
<p>Notion, <b>Head of Marketing</b>, <b>Ideas</b>. On your phone, open the Notion app, find Ideas (star it so it's on your home screen) and tap <b>New</b>.</p>
<p class="small">The database was seeded with 41 ideas from the summer calendar, so it's never empty.</p></div>
<div class="card"><h3>Who can add ideas</h3>
<p>Everyone. Jess, Dan, the team, and the Marketing Project itself, which adds ideas from comments, story replies, reviews and results.</p>
<p class="small">There is no such thing as too small. A single line is enough to start.</p></div>
</div>
<h3>What to drop in</h3>
<div class="grid3">
<div class="card"><b>Customer questions</b><p class="small" style="margin:1mm 0 0">"Can I use it before a run?" Every question is a post, a story or a FAQ.</p></div>
<div class="card"><b>Reviews and messages</b><p class="small" style="margin:1mm 0 0">Paste them word for word with the name as shown. They become proof posts.</p></div>
<div class="card"><b>Moments</b><p class="small" style="margin:1mm 0 0">An event, a season, a race, a stockist visit, a new photo you took.</p></div>
<div class="card"><b>Behind the scenes</b><p class="small" style="margin:1mm 0 0">Making a batch, a new label, Jess with the horses, Dan's guitar.</p></div>
<div class="card"><b>Things you saw</b><p class="small" style="margin:1mm 0 0">A format or trend that would suit us. Add the link.</p></div>
<div class="card"><b>Results</b><p class="small" style="margin:1mm 0 0">"The ankle carousel got 40 saves." Ideas to repeat what works.</p></div>
</div>
'''


def g2_p3(P):
    return f'''
<div class="kicker">Adding an idea</div>
<h2>Fill in what you <span class="hl">know</span></h2>
<p class="lede">Only the <b>Idea</b> title is required. Everything else helps the weekly review place it faster. If you're not sure, leave it blank and the review will suggest it.</p>
<table class="tight">
<tr><th style="width:17%">Field</th><th style="width:38%">What to put</th><th>Example</th></tr>
<tr><td><b>Idea</b> (title)</td><td>One line: what the content is.</td><td>Warm-up before backyard cricket</td></tr>
<tr><td><b>Hook</b></td><td>The headline, if one comes to you.</td><td>"The 20-second warm-up every Boxing Day cricketer needs"</td></tr>
<tr><td><b>Format</b></td><td>Instagram post, Carousel, Reel, Story, Facebook post, FB Live, Email, Blog, Ad, Stockist. Pick more than one if it fits.</td><td>Reel, Story</td></tr>
<tr><td><b>Pillar</b></td><td>Herb science, Injury first aid, How to use, Wellness, Social proof, Founders, Community, Promo anchored in education, Range education.</td><td>How to use</td></tr>
<tr><td><b>Range</b></td><td>Relief, Joints, Sports, All.</td><td>Sports</td></tr>
<tr><td><b>Source</b></td><td>Where it came from: Customer question, Story reply, Comment, Review, Jess and Dan, Head of Marketing, Results, Seasonal date.</td><td>Seasonal date</td></tr>
<tr><td><b>Priority</b></td><td>High, Medium, Low. High means time-sensitive or a proven winner.</td><td>High</td></tr>
<tr><td><b>Target date</b></td><td>When it should go out, if it's tied to a date.</td><td>24 Dec 2026</td></tr>
<tr><td><b>Notes</b></td><td>Anything useful: the review text, a link, a photo file name, who could front it.</td><td>Could film at a family game. Photo idea: bat and Sports Spray on the grass</td></tr>
<tr><td><b>Status</b></td><td>Leave as <b>New</b>. The review and the team move it on.</td><td>New</td></tr>
</table>

<h3>Or just tell the Marketing Project</h3>
<div class="grid2">
<div>{P("""Add this to the Ideas database: [your idea in a sentence].
Source: [where it came from]. Fill in the format, pillar, range and a hook for me.""", "One idea")}</div>
<div>{P("""Here are some ideas from this week. Add each one to the Ideas database as a separate row, with format, pillar, range, source and a draft hook:
[paste your notes, one per line]""", "A brain dump")}</div>
</div>
{P("""Here's a review we got: "[paste word for word]" from [name as shown] on [Judge.me / Google], for [product].
Add it to Ideas as a Social proof idea and suggest which format it suits.""", "A review or customer message")}
'''


def g2_p4(P):
    return f'''
<div class="kicker">Quality and status</div>
<h2>What makes a <span class="hl">good idea</span></h2>
<div class="grid2" style="margin-top:3mm">
<div class="card"><h3>Thin</h3>
<p style="margin:0">"Post about knees"</p>
<p class="small" style="margin:2mm 0 0">No angle, no source, no reason it matters now. The review can only say "needs more detail".</p></div>
<div class="card" style="border-color:var(--green);border-width:2px"><h3>Strong</h3>
<p style="margin:0">"Three customers this month asked if Joints Rub is OK before gardening. Quick Reel: Jess rubs it in, then pulls weeds. Spring/summer gardening season."</p>
<p class="small" style="margin:2mm 0 0">Real question, a format, a person, a reason for now. Ready to shortlist.</p></div>
</div>
<h3>A strong idea answers four questions</h3>
<div class="grid2">
<div class="step"><span class="num">1</span><div><b>What is it?</b> The topic and angle in one line.</div></div>
<div class="step"><span class="num">2</span><div><b>Why now?</b> A season, event, question or trend.</div></div>
<div class="step"><span class="num">3</span><div><b>Where did it come from?</b> A real customer beats a hunch.</div></div>
<div class="step"><span class="num">4</span><div><b>Who could front it?</b> Jess, Dan, a customer, hands only.</div></div>
</div>
<div class="note lime"><b>Check before you add:</b> no new offers (only Jess and Dan set those), no health promises ("cures arthritis" can't become content), and no customer's private details. Public reviews are fine with the name as shown.</div>

<h3>How an idea moves</h3>
<table>
<tr><th style="width:16%">Status</th><th style="width:44%">Means</th><th>Who moves it</th></tr>
<tr><td><b>New</b></td><td>Just added, not reviewed yet.</td><td>Anyone (the default)</td></tr>
<tr><td><b>Shortlisted</b></td><td>Good to go. Skills pick from Shortlisted ideas first.</td><td>The team, after reading the weekly review</td></tr>
<tr><td><b>Planned</b></td><td>Being made, or scheduled. Linked to its Output Log row.</td><td>The Marketing Project, when it drafts the piece</td></tr>
<tr><td><b>Used</b></td><td>Live. The Output field links to the finished piece.</td><td>The Marketing Project, once you tell it it's live</td></tr>
<tr><td><b>Parked</b></td><td>Not now: off-brand, needs info we don't have, or out of season. Add a note why.</td><td>The team</td></tr>
</table>
<p class="small">Parked isn't deleted. Seasonal ideas come back round, and the review will flag parked ideas when their season returns.</p>
'''


def g2_p5(P):
    return f'''
<div class="kicker">Once a week</div>
<h2>What the weekly review <span class="hl">tells you</span></h2>
<p class="lede">The scheduled task runs once a week and posts a short report. Read it at the start of the week and spend 15 minutes
agreeing what to make. It covers six things.</p>
<div class="grid2">
<div class="card"><h3><span class="num">1</span>Do we need more content?</h3>
<p style="margin:0">Checks the next two weeks against the plan: 3 posts a week plus 1 email, and the monthly mix. Shows what's drafted, what's approved and where the gaps are.</p></div>
<div class="card"><h3><span class="num">2</span>New ideas, reviewed</h3>
<p style="margin:0">Every New idea gets a call: shortlist, park, merge with a similar one, or needs more detail. With the format, range and pillar it suits.</p></div>
<div class="card"><h3><span class="num">3</span>Who should make it</h3>
<p style="margin:0">Names who's needed for each piece: the Project to draft, Jess or Dan on camera, someone to build in Canva or film, a customer or ambassador.</p></div>
<div class="card"><h3><span class="num">4</span>What type</h3>
<p style="margin:0">Recommends the format for each idea (a question is often a Reel or carousel, a review a proof post) and the skill to use.</p></div>
<div class="card"><h3><span class="num">5</span>What's trending</h3>
<p style="margin:0">NZ seasons, sport and events coming up, wellness and natural health topics people are searching, and formats working on Instagram and Facebook.</p></div>
<div class="card"><h3><span class="num">6</span>Balance check</h3>
<p style="margin:0">Flags if we're light on a range or pillar, too salesy (80/20), or repeating ourselves. Ends with this week's 3 to 5 actions.</p></div>
</div>

<h3>What a review looks like (example)</h3>
<div class="note" style="font-size:8.6pt;line-height:1.55">
<b>Content health:</b> Week 3 has 2 of 3 posts drafted, no Reel yet. Email for 9 Dec not started. Monthly mix: Reels 1 of 4, carousels 2 of 4.<br>
<b>New ideas (4):</b> "Warm-up before backyard cricket": shortlist as the week 5 Reel, Sports, How to use. Dan on camera, film at a family game.
"Gardening knees": merge with the existing "Kneeling in the garden" idea. "Free shipping over $50": park, offers come from Jess and Dan.<br>
<b>Trending:</b> Great Walks season opens; tramping prep content searches up. Boxing Day cricket. Summer heat and staying active early in the day.<br>
<b>Actions:</b> 1. Shortlist the cricket Reel. 2. Book 20 minutes with Dan to film. 3. Draft the 9 Dec newsletter on kawakawa.
</div>
'''


def g2_p6(P):
    return f'''
<div class="kicker">Roles and targets</div>
<h2>Who does <span class="hl">what</span></h2>
<p class="lede">The review uses these roles when it says who should make a piece. If someone new joins the team, add them here and tell the Project.</p>
<table>
<tr><th style="width:22%">Who</th><th style="width:43%">Does</th><th>Typical content</th></tr>
<tr><td><b>Marketing Project</b><br><span class="small">Claude, Head of Marketing</span></td><td>Drafts every caption, hook, shot list, email and brief. Runs Claims Check. Logs everything. Adds ideas.</td><td>All written content, plans, reports</td></tr>
<tr><td><b>Jess</b></td><td>Approves. On camera and voiceovers. Animal lover and nature enthusiast, did the Rongoā course.</td><td>Herb stories, the horse-rub origin, garden and how-to Reels</td></tr>
<tr><td><b>Dan</b></td><td>Approves. On camera and voiceovers. Rhythm guitarist and amateur philosopher.</td><td>Founders story, "why we do this", honest takes, sport</td></tr>
<tr><td><b>Team member building assets</b></td><td>Builds designs in Canva from the Project's notes. Films and edits. Schedules in Meta Business Suite and builds emails in Shopify Messaging after approval.</td><td>Covers, carousels, story frames, Reel edits</td></tr>
<tr><td><b>Ambassadors</b></td><td>Answer the Introducing Q&A, share photos and their own posts.</td><td>Ambassador series, sport tips</td></tr>
<tr><td><b>Customers and stockists</b></td><td>Reviews, questions, photos (with permission), in-store moments.</td><td>Proof posts, FAQs, stockist features</td></tr>
</table>

<h3>The targets the review checks against</h3>
<div class="grid2">
<table>
<tr><th>Every week</th><th style="width:22%">Target</th></tr>
<tr><td>Posts, cross-posted to Facebook and Instagram</td><td>3</td></tr>
<tr><td>Emails (newsletter or campaign)</td><td>1</td></tr>
<tr><td>Ideas reviewed</td><td>All New</td></tr>
</table>
<table>
<tr><th>Every month</th><th style="width:22%">Target</th></tr>
<tr><td>Reels</td><td>4</td></tr>
<tr><td>Single-image posts / carousels</td><td>4 / 4</td></tr>
<tr><td>Facebook posts</td><td>12</td></tr>
<tr><td>Newsletters + campaign email</td><td>3 + 1</td></tr>
<tr><td>Testimonial graphics</td><td>As reviews come in</td></tr>
</table>
</div>
<p class="small">From the client form and brand spec. If the targets change, update <code>brief/06-brand-spec.md</code> and the review will pick it up.</p>
'''


def g2_p7(P):
    return f'''
<div class="kicker">After the review</div>
<h2>Turn the review into <span class="hl">action</span></h2>
<p class="lede">Open a new chat in the Marketing Project and use these. Then follow the Prompting guide to make each piece.</p>
<div class="grid2">
<div>
{P("""From this week's ideas review: shortlist [idea titles], park [idea titles] with the reason in Notes, and merge [idea] into [idea].""", "Act on the calls")}
{P("""Plan next week using the Shortlisted ideas the review recommended. Use the Weekly Social Content Set skill.""", "Plan the week")}
{P("""Tell me more about the trend "[trend]". Is it right for X-ZONE? If yes, add two ideas for it to the Ideas database with hooks.""", "Explore a trend")}
</div>
<div>
{P("""Write a short message to [Dan / Jess] asking them to film [idea] this week: what to film, where, how long it takes, and the shot list.""", "Brief whoever's needed")}
{P("""Run the ideas review now instead of waiting for the scheduled one.""", "Run it early")}
{P("""Which ideas have been Shortlisted for more than 3 weeks? Should we make them or park them?""", "Clear the backlog")}
</div>
</div>

<h3 style="margin-top:2mm">Summer moments to watch (Nov 2026 to Feb 2027)</h3>
<p class="small" style="margin-top:-1mm">A starting list. The weekly review checks what's actually trending each week.</p>
<table class="tight"><tr><th style="width:24%">When</th><th style="width:36%">Moment</th><th>Angle for X-ZONE</th></tr>
<tr><td>Late Nov to Dec</td><td>Great Walks and tramping season</td><td>Pack list, after-the-walk recovery, Sports and Relief</td></tr>
<tr><td>Dec</td><td>Christmas gifting, pre-Christmas sale</td><td>Gift ideas anchored in education, the sale Jess and Dan set</td></tr>
<tr><td>Boxing Day to Jan</td><td>Backyard cricket, beach sport, holidays</td><td>Warm-ups, first aid for knocks, kids and bumps</td></tr>
<tr><td>Jan</td><td>New year, new routine</td><td>Getting moving again kindly, joints and mornings</td></tr>
<tr><td>Late Jan to Feb</td><td>Back to school and work, Auckland Anniversary</td><td>Desk necks and shoulders, sport season starting</td></tr>
<tr><td>6 Feb</td><td>Waitangi Day</td><td>Only with cultural review. Rongoā content always needs Jess and Dan's sign-off</td></tr>
<tr><td>Feb</td><td>Multisport and triathlon season, summer gardening</td><td>Recovery, Sports range, hands and knees in the garden</td></tr>
</table>
'''


def g2_p8(P):
    return f'''
<div class="kicker">For whoever manages the scheduled task</div>
<h2>The weekly review <span class="hl">prompt</span></h2>
<p class="lede">Your scheduled task is already set up. Compare it with this version and copy across anything it's missing, so every review covers the same
six points. Run it inside the Marketing Project with Notion and GitHub switched on, and web search on for the trends.</p>
{P("""Run the weekly content ideas review for X-ZONE.

1. Load the Role Card, Business Context and Brand Voice & Caption Guide from Notion (Head of Marketing), and brief/06-brand-spec.md and calendar/ from GitHub Xzone-NZ/xzone.
2. Content health: compare the next two weeks of the Output Log and calendar against the targets (3 posts a week cross-posted to Facebook and Instagram, 1 email a week; monthly 4 Reels, 4 single posts, 4 carousels, 12 Facebook posts, 3 newsletters, 1 campaign email). List what's drafted, approved and missing.
3. New ideas: for every idea in the Ideas database with Status New, recommend Shortlist, Park (with a reason), Merge (with which idea) or Needs detail. For each one to shortlist give the format, skill, range, pillar, a hook, a suggested week, and who is needed (Marketing Project, Jess, Dan, the team member building assets, an ambassador or customer). Fill in any blank fields. Do not change Status yourself.
4. Backlog: flag Shortlisted ideas older than 3 weeks, and Parked ideas whose season has come back.
5. Trending: search the web for what's coming up or trending in the next 4 weeks for a NZ natural pain relief brand: NZ seasons, sport and outdoor events, natural health and wellness topics, and formats working on Instagram and Facebook. Suggest up to 5 content ideas from it, add them to Ideas as New (Source: Head of Marketing), and say why each fits.
6. Balance: flag gaps by range and pillar, and whether the mix keeps to 80% educate, 20% sell.
7. End with this week's 3 to 5 actions, each with an owner.

Rules: never suggest an offer Jess and Dan haven't set; anything on te reo Māori or rongoā rākau needs cultural review; keep to the Claims rules. Keep the report under 400 words. Add one line to the Activity Log.""", "Weekly review prompt")}
<div class="grid2">
<div class="card"><h3>Good to know</h3>
<ul style="margin:0"><li>The review recommends; people decide. It does not shortlist or park on its own.</li>
<li>It can only see trends if web search is on for the task.</li>
<li>If Notion or GitHub isn't connected when it runs, it should say so and stop.</li></ul></div>
<div class="card"><h3>Weekly 15-minute routine</h3>
<ol style="margin:0"><li>Read the review.</li><li>Agree shortlist and park calls.</li><li>Book anyone needed on camera.</li><li>Ask the Project to plan the week.</li><li>Send the approval batch to Jess and Dan.</li></ol></div>
</div>
'''


GUIDES = [
    {
        "slug": "xzone-guide-prompting-the-marketing-project",
        "title": "Prompting the Marketing Project",
        "footer": "How to prompt the Marketing Project",
        "cover": {
            "photo": "../brief/photos/jess-dan-garden.jpg", "pos": "center 30%",
            "pill": "Team guide",
            "title": "How to prompt the <span class=\"hl\">Marketing Project</span>",
            "sub": "Copy-ready prompts for newsletters, posts, carousels, Reels, stories, emails and more. Ask well once, get a draft Jess and Dan can approve.",
            "for": "the X-ZONE marketing team", "version": "November 2026",
        },
        "pages": [g1_p2, g1_p3, g1_p4, g1_p5, g1_p6, g1_p7, g1_p8, g1_p9, g1_p10, g1_p11, g1_p12],
    },
    {
        "slug": "xzone-guide-ideas-and-weekly-review",
        "title": "Ideas and the Weekly Review",
        "footer": "The Ideas database and weekly review",
        "cover": {
            "photo": "../brief/photos/relief-rub-leg.jpg", "pos": "center",
            "pill": "Team guide",
            "title": "Every idea, <span class=\"hl\">reviewed weekly</span>",
            "sub": "How to drop ideas into the Ideas database, what the weekly review tells you, who makes what, and how to act on it.",
            "for": "the X-ZONE marketing team", "version": "November 2026",
        },
        "pages": [g2_p2, g2_p3, g2_p4, g2_p5, g2_p6, g2_p7, g2_p8],
    },
]
