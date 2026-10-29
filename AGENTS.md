# Grimoire

A knowledge base built from video transcripts. Everything here is what some video said, so answer
from the videos, in their words where it matters, and say when they disagree or when none of them
covers the question.

## Layout

- `sources.txt` - one YouTube or Twitch URL, playlist or channel per line. `python fetch.py` pulls captions.
- `transcripts/<date>_<id>_<title>.txt` - one file per video. Header lines (`# title`, `# channel`,
  `# date`, `# url`), then paragraphs that start with a `[m:ss]` mark.
- `notes/INDEX.md` - one line per digested video: `- <id> | <channel> | <title> | <topics>`.
- `notes/<id>.md` - the digest of one video (see below).

## Answering a question

1. Read `notes/INDEX.md` and pick the videos whose topics match.
2. Read those notes. If a note settles the question, answer from it.
3. For detail, or when notes disagree, grep `transcripts/` for the hero, item or term and read the hits
   with a few paragraphs of context. Transcripts are auto captions: names are often misheard
   (search a few spellings) and nothing is punctuated.
4. Answer in plain words. Lead with what to do. Say which channel said it when sources disagree.
   Never add a claim no transcript supports. "No video covers this" is a fine answer.

## Digesting new transcripts

For each transcript with no `notes/<id>.md` (or on request), read it and write the note:

```
# <title>
channel: <channel>  date: <date>  url: <url>

## Covers
<heroes, items, topics, one line>

## Claims
- <one claim per bullet, in the speaker's terms, with the [m:ss] it came from>

## Disagrees with
- <any claim that contradicts another note, naming that note's id> (or "none found")
```

Keep claims as the speaker gave them: what a hero wants in lane, when it spikes, what to buy, what to
do against it, macro rules (when to fight, rotate, take objectives). Skip banter and sponsor reads.
Then add the video's line to `notes/INDEX.md`. A thousand transcripts is a thousand reads: digest in
batches, newest or most asked about first, and leave the rest for when a question reaches them.

## Style

No em dashes anywhere (use "-"). Hero and item names as the game spells them.
