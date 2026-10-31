# Grimoire

Paste video links. Get transcripts and notes that a coding assistant can answer questions from.

It works for any game or subject. The transcripts are plain text, the index is a Markdown file, and
the search is the grep your assistant already has. You don't need a database, a model of your own,
or an API key.

## Setup

```
pip install yt-dlp
git clone <this repo>
cd grimoire
```

## Use

1. Put links in `sources.txt`, one per line. Single videos, playlists and channels all work, from
   YouTube or Twitch. If YouTube answers "sign in to confirm you're not a bot", run
   `python fetch.py --cookies chrome` (or firefox, edge) so it uses your signed-in browser.
2. Run `python fetch.py`. One `.txt` per video lands in `transcripts/`. Videos you already fetched are
   skipped, and videos with no English captions are listed at the end. Channels carry off-topic videos,
   so for a whole channel add `--keep-only <word>` (for example `--keep-only deadlock`) to drop any
   transcript that never mentions your subject.
3. Open the folder in your coding assistant and ask it to digest the new transcripts. It follows
   `AGENTS.md`: a short note per video in `notes/`, and one line per video in `notes/INDEX.md`.
4. Ask questions. The assistant reads the index, then the notes, then the transcripts when it needs
   the exact words.

`python fetch.py --selftest` checks the caption-to-text step.

## What goes in the repo

Commit `sources.txt`, `transcripts/` and `notes/`. `raw/` is scratch and is ignored.
