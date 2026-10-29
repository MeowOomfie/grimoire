"""Pull captions for every link in sources.txt and write one plain-text transcript per video.

    python fetch.py              # reads sources.txt
    python fetch.py mylist.txt   # any file: one YouTube / Twitch URL, playlist or channel per line
    python fetch.py --cookies chrome   # when YouTube says "sign in to confirm you're not a bot"
    python fetch.py --selftest   # checks the caption-to-text conversion on a built-in sample

Needs yt-dlp on PATH (pip install yt-dlp). No video is downloaded, only captions.
Videos already fetched are skipped (raw/archive.txt). Videos without captions are reported and skipped.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "transcripts"
PARAGRAPH_SECONDS = 30  # a [m:ss] mark roughly every half minute

CUE = re.compile(r"(\d+):(\d\d):(\d\d)\.\d+ --> ")
TAG = re.compile(r"<[^>]+>")


def vtt_to_text(vtt: str) -> str:
    """Caption cues to paragraphs, each starting with its [m:ss] mark.

    Auto captions roll: every cue repeats the previous line and adds one, so a line equal to the
    last kept line is dropped. Inline timing tags (<00:00:01.000><c>) are stripped.
    """
    paragraphs, current, para_start, last = [], [], None, ""
    t = None
    for line in vtt.splitlines():
        m = CUE.match(line)
        if m:
            h, mi, s = map(int, m.groups())
            t = h * 3600 + mi * 60 + s
            continue
        if t is None or not line.strip() or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        text = TAG.sub("", line).replace("&nbsp;", " ").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").strip()
        if not text or text == last:
            continue
        if para_start is None or t - para_start >= PARAGRAPH_SECONDS:
            if current:
                paragraphs.append(f"[{para_start // 60}:{para_start % 60:02d}] " + " ".join(current))
            current, para_start = [], t
        current.append(text)
        last = text
    if current:
        paragraphs.append(f"[{para_start // 60}:{para_start % 60:02d}] " + " ".join(current))
    return "\n\n".join(paragraphs) + "\n"


def slug(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-")[:70] or "untitled"


def read_meta() -> dict:
    meta = {}
    p = RAW / "meta.tsv"
    if p.exists():
        for row in p.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = row.split("\t")
            if len(parts) == 5:
                meta[parts[0]] = parts
    return meta


def convert_all() -> int:
    OUT.mkdir(exist_ok=True)
    meta = read_meta()
    done = 0
    for vtt in sorted(RAW.glob("*.vtt")):
        vid = vtt.name.split("_", 2)[1] if vtt.name.count("_") >= 2 else vtt.stem
        _, channel, title, date, url = meta.get(vid, (vid, "", vtt.stem, "", ""))
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}" if len(date) == 8 else "unknown-date"
        target = OUT / f"{date}_{vid}_{slug(title)}.txt"
        if not target.exists():
            body = vtt_to_text(vtt.read_text(encoding="utf-8", errors="replace"))
            header = f"# {title}\n# channel: {channel}\n# date: {date}\n# url: {url}\n\n"
            target.write_text(header + body, encoding="utf-8")
            done += 1
        vtt.unlink()
    return done


def fetch(sources: Path, cookies: str | None) -> None:
    RAW.mkdir(exist_ok=True)
    cmd = [
        "yt-dlp", "--skip-download", "--write-sub", "--write-auto-sub", "--sub-langs", "en.*",
        *(["--cookies-from-browser", cookies] if cookies else []),
        "--sub-format", "vtt", "--ignore-errors", "--no-warnings",
        "--download-archive", str(RAW / "archive.txt"), "--force-write-archive",
        "--print-to-file", "%(id)s\t%(channel)s\t%(title)s\t%(upload_date)s\t%(webpage_url)s", str(RAW / "meta.tsv"),
        "-o", str(RAW / "%(upload_date)s_%(id)s_%(title).70s.%(ext)s"),
        "-a", str(sources),
    ]
    subprocess.run(cmd, check=False)  # ignore-errors: one bad link must not stop the batch
    n = convert_all()
    have = {p.name.split("_", 2)[1] for p in OUT.glob("*_*_*.txt")}
    missing = sorted(set(read_meta()) - have)
    print(f"\n{n} new transcript(s), {len(have)} total in {OUT.name}/")
    if missing:
        print(f"{len(missing)} video(s) had no English captions and were skipped: {' '.join(missing)}")


SAMPLE = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:03.000
Mina wants<00:00:02.000><c> to farm</c>

00:00:03.000 --> 00:00:05.000
Mina wants to farm
don't trade with her

00:00:05.000 --> 00:00:07.000
don't trade with her

00:00:35.000 --> 00:00:37.000
at twenty she wins
"""


def selftest() -> None:
    got = vtt_to_text(SAMPLE)
    want = "[0:01] Mina wants to farm don't trade with her\n\n[0:35] at twenty she wins\n"
    assert got == want, f"\n--- got ---\n{got}\n--- want ---\n{want}"
    assert slug("Every Hero's REAL Role (2026)") == "Every-Hero-s-REAL-Role-2026"
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        args = sys.argv[1:]
        cookies = args.pop(args.index("--cookies") + 1) if "--cookies" in args else None
        args = [a for a in args if a != "--cookies"]
        src = Path(args[0]) if args else HERE / "sources.txt"
        if not src.exists():
            sys.exit(f"{src} not found: put one URL per line in it")
        fetch(src, cookies)
