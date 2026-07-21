# LinkedIn post — King County EDA

Copy the post body below, attach `EDA_Project_Presentation.pdf` as a **document post**
(LinkedIn renders it as a swipeable carousel and reaches far more people than a link),
and put the repo link in the first comment.

---

## Primary post

> **Hook check:** LinkedIn truncates at roughly two lines before "…see more".
> The first sentence has to carry the whole post. It does.

```
My client wanted a waterfront mansion she could flip within a year.

The data told her not to flip it. I put that on slide 8.

I spent a week on the King County housing dataset — 21,597 sales, May 2014 to
May 2015 — acting as the analyst for a buyer with six hard requirements: high
budget, waterfront, renovated, high grade, buy within a month, resell within
a year.

Three things I found:

→ Waterfront isn't a feature, it's a separate market. Median $1.51M against
$450K — a 3.4x premium on 0.7% of the housing stock.

→ Renovation pays: +35% market-wide, +64% in the luxury segment. It's the one
price finding that survived a confounder check — split the market into
living-area bands and the premium holds in every band above 1,500 sqft.

→ Her six requirements, applied together, left 5 properties out of 21,597.
The scarcity was itself the answer: the brief was close to unsatisfiable, and
she needed to know which requirement to relax.

But the part I'm actually proud of is what I threw away.

I found a "best day of the month to buy" — day 10, median $1.26M. It rested on
7 sales. A permutation test reproduced a gap that large 74% of the time, and
across all 21,597 sales day 10 turned out to be the 28th cheapest of 31. The
pattern reversed the moment it had real data behind it.

Same story for "sell in September, +43%." Market-wide, that gap is +1.8%. The
seasonal effect is statistically real and economically irrelevant — significance
answers "is it real", effect size answers "do I care", and here the answers were
yes and no.

Then the resale plan. 176 houses in the dataset sold twice. Five sat in my
client's price and grade segment, returning +7.1%, +6.5%, +1.9%, +1.4%, -0.8% —
a median of +1.9% over six months, against 6-10% in round-trip transaction
costs. The tempting market-wide figure of +54% comes almost entirely from
low-end flips, which is a completely different business from buying a $4M
waterfront property.

So the recommendation was: buy it, but buy it to hold.

Two of my seven hypotheses were rejected, and the deck is better for it. Anyone
can find a pattern in 240 rows. Testing whether it survives contact with the
full dataset is the job.

Full notebook, the permutation tests, and the slide deck are in the repo —
link in the comments. Feedback welcome, especially the critical kind.

(Bootcamp capstone. The client is fictional; the data and the mistakes are real.)

#DataAnalysis #EDA #Python #pandas #DataScience #Statistics #RealEstateAnalytics
```

---

## Shorter variant (if the long one feels heavy)

```
I found a "best day of the month to buy a house." Then I deleted it from my
own presentation.

Day 10 had the lowest median luxury price in the King County dataset —
$1.26M. It rested on 7 sales. A permutation test reproduced a gap that large
74% of the time, and across all 21,597 sales, day 10 was the 28th cheapest
of 31 days. The pattern reversed the moment it had real data behind it.

Same for "sell in September, +43% premium." Market-wide that gap is +1.8%.
Statistically real, economically irrelevant.

What did survive testing:
→ Waterfront: 3.4x price premium, on 0.7% of the stock
→ Renovation: +35% market-wide, +64% luxury — and it holds after controlling
   for house size
→ My client's six requirements left 5 qualifying properties out of 21,597

And the finding she didn't want: repeat sales in her segment returned a median
+1.9% over six months, against 6-10% transaction costs. The one-year flip
doesn't pay. I told her.

Two of seven hypotheses rejected. That's the part I'd want a hiring manager
to read.

Notebook + deck in the comments.

(Bootcamp capstone, fictional client, real data.)

#DataAnalysis #EDA #Python #pandas #Statistics #DataScience
```

---

## First comment (post this immediately after)

```
Repo: https://github.com/PartORG/eda_project_bootcamp

Stack: PostgreSQL → pandas → matplotlib/seaborn/folium, dependencies managed
with uv. The notebook runs top to bottom on a fresh kernel, and the slide deck
is generated from the same CSV by a script, so the numbers on the slides can't
drift from the analysis.

Happy to talk through the permutation test — it's ~10 lines of NumPy and it's
what turned two confident recommendations into two rejections.
```

---

## Posting notes

| | |
|---|---|
| **Format** | Document post — upload the PDF directly. Don't post a link to it. |
| **Links** | Put the repo URL in the first comment, not the body. |
| **Timing** | Tuesday–Thursday, 08:00–10:00 local. |
| **First hour** | Reply to every comment; early engagement drives reach. |
| **Hashtags** | 4–6 max. More reads as spam. |

**Before you post, confirm:**

- [ ] Credentials purged from git history and the bootcamp password rotated
- [ ] Repo is public and the README renders correctly on GitHub
- [ ] Deck regenerated from your real `data/eda.csv`
- [ ] The "fictional client" line is present — the deck's invented agency and
      job titles read as satire in context, but not to a stranger scrolling past

**Why this post is built around the rejections:** every bootcamp graduate posts
"I analysed a housing dataset and here are my three insights." Almost nobody
posts "I found an insight, tested it, and it evaporated." The second one is
evidence of judgment, and judgment is the thing that's actually hard to hire for.
