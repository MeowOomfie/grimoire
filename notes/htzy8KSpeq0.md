# How to Have Multiple Ping Wheels in Deadlock
channel: Midknight
date: 2025-09-22
url: https://www.youtube.com/watch?v=htzy8KSpeq0

## Covers
A settings walkthrough (September 2025) for binding up to four ping wheels you toggle between with keys, using an autoexec.cfg and per-wheel cfg files in the game's config folder. Works on Windows and Linux; shown on Windows.

## Claims
- You can set keyboard keys that toggle between up to four ping wheels; middle click still opens the current wheel. [0:00]
- The method works on Linux and Windows in pretty much the same way. [0:00]
- Step 1: in Steam, right-click Deadlock, Properties, Installed Files, Browse. [0:31]
- Step 2: open game, then citadel, then cfg (config), and keep that folder open. [0:31]
- Step 3: open Notepad and paste the autoexec text from the video description (also pinned in his Discord). [1:01]
- The number of wheel entries in that text is the total number of ping wheels, not additional ones; delete the ping wheel 3 and 4 lines if you want two. [1:31]
- The bind entries are the toggle keys, default H and J; change them to any key (for example I, O, P), but avoid keys already bound in Deadlock or it can get funky. [1:31]
- Step 4: File, Save As, name it autoexec.cfg, set Save as type to All files, save (desktop recommended). [2:01]
- Step 5: drag autoexec.cfg into the cfg folder. [2:31]
- Step 6: in the cfg folder create a new folder named ping_wheels, all lowercase (caps probably matter). [2:31]
- Step 7: in Notepad type anything, Save As 1.cfg with Save as type All files, and drag it into ping_wheels; a file shown as "1" of type CFG file is fine. [3:01]
- Step 8: copy that file and rename the copy 2 (and 3, 4 for more wheels), one file per wheel set up in autoexec. [3:31]
- Step 9: in each wheel file paste the ping_wheel_phrase lines from the description, then add a ping ID after each. [4:02]
- Ping IDs come from a website linked in the description; for example ping "No" is ID 17 and "Can heal" is 33. [4:32]
- Slot 0 is the top of the wheel, then slots 1 to 7 go clockwise. [4:32]
- Put a space between the end of the phrase and the ID number. [5:02]
- Save each wheel file before closing it. [5:33]
- Launch Deadlock and press the bound keys (default H and J) to toggle between wheels. [6:03]
- The bind keys toggle between wheels; they are not the key you press to open the ping wheel. [7:05]
- If it doesn't work, recheck file names and locations, try different bind keys, and restart your system. [7:05]
- Credit for the method goes to Farewell Nuke. [4:32]

## Disagrees with
- none recorded yet
