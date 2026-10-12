#!/usr/bin/env python3
"""
Allegra Grant site builder — allegragrant.com

TO ADD A BOOK: add a row to ZODIAC or STANDALONE below and re-run.
TO CHANGE THE LEAD TITLE: edit FEATURED.
Nothing else needs to change.
"""
import json, urllib.parse, pathlib

# ===================================================================
#  PASTE THE ACTIVECAMPAIGN EMBED CODE BETWEEN THE TRIPLE QUOTES.
#  Leave it empty and the signup section falls back to a button that
#  sends people to the existing Wix opt-in page, so the funnel keeps
#  working either way.
#    ActiveCampaign -> Website -> Forms -> your form -> Integrate
# ===================================================================
FORM_EMBED = """<form class="ac" method="POST" action="https://allegragrant.activehosted.com/proc.php" target="_blank">
  <input type="hidden" name="u" value="1">
  <input type="hidden" name="f" value="1">
  <input type="hidden" name="s" value="">
  <input type="hidden" name="c" value="0">
  <input type="hidden" name="m" value="0">
  <input type="hidden" name="act" value="sub">
  <input type="hidden" name="v" value="2">
  <label class="sr-only" for="ac-firstname">First name</label>
  <input id="ac-firstname" type="text" name="firstname" placeholder="Your first name" autocomplete="given-name">
  <label class="sr-only" for="ac-email">Email address</label>
  <input id="ac-email" type="email" name="email" placeholder="Your email" required autocomplete="email">
  <button type="submit">Send me the list!</button>
</form>"""

FALLBACK_OPTIN = "https://guy996.wixsite.com/allegragrant"

SITE   = "https://allegragrant.com/"
AUTHOR = "Allegra Grant"

# (label, sub-label, url)
SOCIAL = [
    ("Facebook", "Allegra Grant, Crystal Girl",
     "https://www.facebook.com/AllegraGrantCrystalGirl"),
    ("Facebook Group", "Healing Crystals Changed My Dang Life",
     "https://www.facebook.com/groups/healingcrystalschangedmydanglife"),
    ("TikTok", "@AllegraGrantBooks",
     "https://www.tiktok.com/@AllegraGrantBooks"),
]

# ============================== DATA ==============================

# The lead title, shown above the zodiac series.
# Guy's strongest seller, especially over the holidays.
FEATURED = {
    "title": "Crystals and Gemstones for Kids and Teens",
    "asin":  "B0B1M1BN2Z",
    "blurb": ("A beginner’s guide to the healing and self-care magic of crystals, gems and "
              "stones — written for ages 8 and up, and for the grown-ups reading along. "
              "Every stone’s meaning in plain language, plus the chakra and birth-sign "
              "stones kids ask about first."),
    "audio": True,
}

# (sign, glyph, dates, element, ASIN, has_audiobook)
ZODIAC = [
    ("Aries",       "♈", "March 21 – April 19",       "Fire",  "B0FL84HL9K", False),
    ("Taurus",      "♉", "April 20 – May 20",         "Earth", "B0FLKK2GXM", False),
    ("Gemini",      "♊", "May 21 – June 20",          "Air",   "B0DDLGJ7CD", False),
    ("Cancer",      "♋", "June 21 – July 22",         "Water", "B0D7CDRN5B", False),
    ("Leo",         "♌", "July 23 – August 22",       "Fire",  "B0DDLG7BMJ", True),
    ("Virgo",       "♍", "August 23 – September 22",  "Earth", "B0FLKKLDBL", False),
    ("Libra",       "♎", "September 23 – October 22", "Air",   "B0FLF2MC9H", False),
    ("Scorpio",     "♏", "October 23 – November 21",  "Water", "B0FLKG4ND6", False),
    ("Sagittarius", "♐", "November 22 – December 21", "Fire",  "B0FLF58B39", False),
    ("Capricorn",   "♑", "December 22 – January 19",  "Earth", "B0FL9DHD99", False),
    ("Aquarius",    "♒", "January 20 – February 18",  "Air",   "B0FL84DYYB", False),
    ("Pisces",      "♓", "February 19 – March 20",    "Water", "B0FLF3JM98", False),
]

# (title, ASIN, blurb, has_audiobook)
STANDALONE = [
    ("Crystals for the Mind", "B09CNRVPVP",
     "Twenty-seven crystals, stones and gems for anxiety and stress — what each one is "
     "for, and how to actually use it.", True),
    ("Your First Spell Jar (and 59 more…)", "B0BL8CXY45",
     "Sixty magickal recipes for the beginner witch, using crystals, herbs, candles and oils. "
     "Protection, prosperity, happiness, power and love.", True),
]

# ============================ END DATA ============================

def amazon(asin):
    return "https://www.amazon.com/dp/" + asin

def audible(title):
    return "https://www.audible.com/search?" + urllib.parse.urlencode(
        {"keywords": title, "searchAuthor": AUTHOR})

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

# ---- featured block
F = FEATURED
featured_html = """      <div class="feat-video">
        <video controls preload="none" playsinline
               poster="media/crystals-kids-poster.jpg"
               aria-label="Short video about %s">
          <source src="media/crystals-kids-ad.mp4" type="video/mp4">
          <a href="%s" rel="noopener">See the book on Amazon</a>
        </video>
      </div>
      <div class="feat-body">
        <p class="feat-eyebrow">Her most-read book · Ages 8 and up</p>
        <h2>%s</h2>
        <p>%s</p>
        <div class="btns">
          <a class="btn" href="%s" rel="noopener">Read</a>
          <a class="btn alt" href="%s" rel="noopener">Listen</a>
        </div>
      </div>""" % (esc(F["title"]), amazon(F["asin"]), esc(F["title"]),
                   esc(F["blurb"]), amazon(F["asin"]), audible(F["title"]))

# ---- the twelve signs
sign_cards = []
for name, glyph, dates, element, asin, audio in ZODIAC:
    chip = '<span class="chip">Audiobook</span>' if audio else ""
    sign_cards.append("""      <article class="sign el-%s">
        <a class="sign-link" href="%s" rel="noopener">
          <img src="covers/%s.webp" width="150" height="240" alt="Cover of the %s Self-care Encyclopedia" loading="lazy">
          <div class="sign-meta">
            <span class="glyph" aria-hidden="true">%s</span>
            <h3>%s</h3>
            <p class="dates">%s</p>
            <p class="element">%s</p>
            %s
          </div>
        </a>
      </article>""" % (element.lower(), amazon(asin), asin, esc(name), glyph,
                       esc(name), esc(dates), element, chip))

# ---- remaining standalones
book_cards = []
for title, asin, blurb, audio in STANDALONE:
    listen = '<a class="btn alt" href="%s" rel="noopener">Listen</a>' % audible(title) if audio else ""
    book_cards.append("""      <article class="book">
        <img src="covers/%s.webp" width="170" height="272" alt="Cover of %s" loading="lazy">
        <div class="book-body">
          <h3>%s</h3>
          <p>%s</p>
          <div class="btns">
            <a class="btn" href="%s" rel="noopener">Read</a>
            %s
          </div>
        </div>
      </article>""" % (asin, esc(title), esc(title), esc(blurb), amazon(asin), listen))

social_html = " \u00b7 ".join(
    '<a href="%s" rel="noopener me">%s</a>' % (url, esc(name))
    for _net, name, url in SOCIAL)

if FORM_EMBED.strip():
    form_block = '<div class="ac-form">%s</div>' % FORM_EMBED
else:
    form_block = ('<a class="btn" href="%s" rel="noopener">Send me the guide</a>'
                  % FALLBACK_OPTIN)

signup_html = '''      <img class="guide-cover" src="media/crystal-guide.webp" width="220" height="351"
           alt="Cover of The Complete Guide to Cleansing and Charging Your Crystals" loading="lazy">
      <div class="signup-body">
        <p class="feat-eyebrow">Free guide</p>
        <h2>The Complete Guide to Cleansing &amp; Charging Your Crystals</h2>
        <p>Why you should care for your crystals, a complete list of cleansing and charging
        methods, and the practices I actually use myself. Free \u2014 I\u2019ll email it to you.</p>
        %s
      </div>''' % form_block

DESC = ("Allegra Grant writes everyday self-care guides built on astrology, crystals, essential "
        "oils and a little witchcraft — Crystals and Gemstones for Kids and Teens, the "
        "twelve-book Zodiac Self-care Encyclopedia, Crystals for the Mind, and Your First Spell Jar.")

CSS = """
:root{
  --ground:#141A17; --surface:#1C2420;
  --ink:#EFE9DC; --muted:#99A398; --rule:#2E3833;
  --accent:#C8A04E;
  --fire:#D08A45; --earth:#8FA167; --air:#8FB0C2; --water:#6B98A4;
}
*{box-sizing:border-box;}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;}}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"DM Sans",system-ui,-apple-system,sans-serif; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
.site{padding-left:20px;padding-right:20px;}
.wrap{max-width:1080px;margin:0 auto;}
img{max-width:100%;display:block;}
a{color:inherit;}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;}

.masthead{padding-block:72px 44px;}
.eyebrow{font-size:10.5px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin:0 0 20px;}
h1{font-family:"Gloock",Georgia,serif;font-weight:400;font-size:clamp(2.9rem,8.5vw,5.2rem);
   line-height:1.0;margin:0 0 20px;text-wrap:balance;}
.standfirst{font-family:"Gloock",Georgia,serif;font-size:clamp(1.1rem,2.3vw,1.4rem);
   line-height:1.45;margin:0 0 18px;max-width:38ch;}
.bio{font-size:15.5px;line-height:1.75;color:var(--muted);margin:0;max-width:60ch;}
.bio strong{color:var(--ink);font-weight:500;}

.byline{display:flex;align-items:flex-start;gap:18px;margin-top:4px;}
.byline img{width:76px;height:76px;flex:0 0 auto;border-radius:50%;
  background:rgba(200,160,78,.10);border:1px solid var(--rule);}

.feat-video video{width:100%;height:auto;aspect-ratio:16/9;display:block;border-radius:5px;
  background:#0C100E;box-shadow:0 18px 44px rgba(0,0,0,.6);}

.elsewhere a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--rule);}
.elsewhere a:hover{color:var(--accent);border-bottom-color:var(--accent);}

.signup{display:grid;grid-template-columns:220px 1fr;gap:38px;align-items:center;
  padding-block:52px;border-bottom:1px solid var(--rule);}
.guide-cover{width:100%;height:auto;border-radius:4px;box-shadow:0 14px 36px rgba(0,0,0,.55);}
.signup-body h2{font-family:"Gloock",Georgia,serif;font-weight:400;
  font-size:clamp(1.4rem,3vw,2rem);line-height:1.18;margin:0 0 14px;}
.signup-body > p:not(.feat-eyebrow){font-size:15.5px;line-height:1.7;color:var(--muted);
  margin:0 0 22px;max-width:50ch;}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0;}
.ac-form form{display:flex;flex-wrap:wrap;gap:9px;align-items:center;max-width:540px;}
.ac-form input[type=text],.ac-form input[type=email]{
  background:var(--surface);border:1px solid var(--rule);color:var(--ink);
  padding:12px 13px;border-radius:3px;font:inherit;font-size:14px;margin:0;flex:1 1 180px;min-width:0;}
.ac-form input[type=submit],.ac-form button{
  background:var(--ink);color:var(--ground);border:0;padding:12px 18px;border-radius:2px;
  font:inherit;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;cursor:pointer;flex:0 0 auto;}
.ac-form input[type=submit]:hover,.ac-form button:hover{background:var(--accent);}

.featured{display:grid;grid-template-columns:1.25fr 1fr;gap:44px;align-items:center;
  padding-block:52px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);}
.feat-cover img{width:100%;height:auto;border-radius:4px;box-shadow:0 18px 44px rgba(0,0,0,.6);
  transition:transform .2s ease;}
.feat-cover:hover img{transform:translateY(-5px);}
.feat-eyebrow{font-size:10.5px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin:0 0 16px;}
.feat-body h2{font-family:"Gloock",Georgia,serif;font-weight:400;
  font-size:clamp(1.7rem,4vw,2.6rem);line-height:1.12;margin:0 0 16px;}
.feat-body > p:not(.feat-eyebrow){font-size:16px;line-height:1.7;color:var(--muted);
  margin:0 0 24px;max-width:52ch;}

section{padding-block:56px;border-bottom:1px solid var(--rule);}
.section-head{margin-bottom:34px;}
.section-head h2{font-family:"Gloock",Georgia,serif;font-weight:400;
   font-size:clamp(1.5rem,3.4vw,2.1rem);margin:0 0 10px;}
.section-head p{margin:0;font-size:14.5px;line-height:1.65;color:var(--muted);max-width:54ch;}

.wheel{display:grid;grid-template-columns:repeat(2,1fr);gap:26px 18px;align-items:start;}
@media (min-width:620px){.wheel{grid-template-columns:repeat(3,1fr);}}
@media (min-width:880px){.wheel{grid-template-columns:repeat(4,1fr);}}
.sign-link{display:block;text-decoration:none;}
.sign img{border-radius:3px;box-shadow:0 8px 22px rgba(0,0,0,.5);transition:transform .18s ease;width:100%;height:auto;}
.sign-link:hover img{transform:translateY(-4px);}
.sign-meta{padding-top:13px;}
.glyph{font-size:19px;line-height:1;color:var(--accent);display:inline-block;margin-bottom:5px;}
.sign h3{font-family:"Gloock",Georgia,serif;font-weight:400;font-size:1.22rem;margin:0 0 3px;}
.dates{margin:0;font-size:12.5px;color:var(--muted);font-variant-numeric:tabular-nums;}
.element{margin:7px 0 0;font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;}
.el-fire .element{color:var(--fire);}
.el-earth .element{color:var(--earth);}
.el-air .element{color:var(--air);}
.el-water .element{color:var(--water);}
.chip{display:inline-block;margin-top:8px;font-size:9.5px;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;padding:4px 7px;border-radius:2px;border:1px solid var(--accent);color:var(--accent);}

.books{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);}
.book{background:var(--surface);padding:26px 24px;display:flex;gap:20px;align-items:flex-start;}
.book img{flex:0 0 auto;width:120px;border-radius:3px;box-shadow:0 6px 18px rgba(0,0,0,.45);}
.book-body{min-width:0;}
.book h3{font-family:"Gloock",Georgia,serif;font-weight:400;font-size:1.16rem;margin:0 0 9px;line-height:1.3;}
.book p{margin:0 0 15px;font-size:14px;line-height:1.65;color:var(--muted);}

.btns{display:flex;flex-wrap:wrap;gap:8px;}
.btn{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  background:var(--ink);color:var(--ground);text-decoration:none;padding:11px 17px;border-radius:2px;
  transition:background .15s,color .15s;}
.btn:hover{background:var(--accent);color:var(--ground);}
.btn.alt{background:transparent;color:var(--ink);border:1px solid var(--rule);}
.btn.alt:hover{border-color:var(--accent);color:var(--accent);background:transparent;}

footer{padding-block:42px 68px;}
footer p{font-size:13.5px;line-height:1.7;color:var(--muted);margin:0 0 9px;max-width:64ch;}

@media (max-width:720px){
  .featured{grid-template-columns:1fr;gap:26px;}
  .signup{grid-template-columns:1fr;gap:24px;}
  .guide-cover{max-width:180px;}
  .byline{gap:14px;}
  .byline img{width:60px;height:60px;}
}
@media (max-width:430px){
  .book{flex-direction:column;}
}
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Allegra Grant — Astrology &amp; Everyday Self-Care</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__SITE__">
<meta property="og:type" content="profile">
<meta property="og:title" content="Allegra Grant — Astrology &amp; Everyday Self-Care">
<meta property="og:description" content="Crystals and Gemstones for Kids and Teens, the twelve-book Zodiac Self-care Encyclopedia, and guides to crystals and spell jars.">
<meta property="og:url" content="__SITE__">
<meta property="og:image" content="__SITE__covers/B0B1M1BN2Z.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23141A17'/><text x='16' y='24' font-size='22' font-family='Georgia,serif' fill='%23C8A04E' text-anchor='middle'>A</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gloock&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&display=swap">
<style>__CSS__</style>
</head>
<body>
<div class="site">
<div class="wrap">

  <header class="masthead">
    <p class="eyebrow">Astrology · Crystals · Everyday Ritual</p>
    <h1>Allegra&nbsp;Grant</h1>
    <p class="standfirst">Self-care you can actually do on a Tuesday.</p>
    <div class="byline">
      <img src="media/allegra-avatar.webp" width="76" height="76" alt="Allegra Grant" loading="lazy">
      <p class="bio">Hey everyone, I’m Allegra, and I’m a crystal girl. I got started on this path a few years ago — after a few glasses of red wine — when I stumbled into a crystal shop in New York City, and well, my whole life changed. Everything I’ve learned since has gone into these books: <strong>crystals, essential oils, herbs, chakras, tarot, yoga, affirmations, and a little witchcraft</strong>. No mystique, no gatekeeping, nothing you need to already believe. Just what to do, and why it’s worth doing.</p>
    </div>
  </header>

  <div class="featured">
__FEATURED__
  </div>

  <section id="zodiac">
    <div class="section-head">
      <h2>The Zodiac Self-care Encyclopedia</h2>
      <p>Twelve books, one for every sign — each a complete set of rituals built for that sign specifically. Find yours.</p>
    </div>
    <div class="wheel">
__WHEEL__
    </div>
  </section>

  <section id="books">
    <div class="section-head">
      <h2>Crystals &amp; Spells</h2>
      <p>Two more standalone guides, for readers who want to go further.</p>
    </div>
    <div class="books">
__BOOKS__
    </div>
  </section>

  <div class="signup">
__SIGNUP__
  </div>

  <footer>
    <p>Available on Kindle and in paperback, with audiobook editions for the three standalone guides and the Leo Self-care Encyclopedia.</p>
    <p>Nothing here is medical, psychological, or financial advice. Crystals and rituals are a complement to care, never a replacement for it.</p>
    <p class="elsewhere">Write to Allegra anytime: <a href="mailto:info@AllegraGrant.com">info@AllegraGrant.com</a></p>
    <p class="elsewhere">Elsewhere: __SOCIAL__</p>
    <p>Published by GO Publishing LLC.</p>
  </footer>

</div>
</div>

<script type="application/ld+json">
__LD__
</script>
</body>
</html>
"""

LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Allegra Grant",
    "url": SITE,
    "jobTitle": "Author",
    "description": ("Author of Crystals and Gemstones for Kids and Teens and the twelve-book "
                    "Zodiac Self-care Encyclopedia."),
    "sameAs": [u for _, _, u in SOCIAL],
}, indent=2)

html = (PAGE.replace("__DESC__", esc(DESC))
            .replace("__SITE__", SITE)
            .replace("__CSS__", CSS)
            .replace("__FEATURED__", featured_html)
            .replace("__WHEEL__", "\n".join(sign_cards))
            .replace("__BOOKS__", "\n".join(book_cards))
            .replace("__SOCIAL__", social_html)
            .replace("__SIGNUP__", signup_html)
            .replace("__LD__", LD))

out = pathlib.Path(__file__).parent / "index.html"
out.write_text(html, encoding="utf-8")
print("wrote %s  (featured + %d signs + %d standalone = %d titles, %d bytes)"
      % (out, len(ZODIAC), len(STANDALONE), 1 + len(ZODIAC) + len(STANDALONE), len(html)))
