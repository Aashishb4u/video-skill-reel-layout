---
name: aashish-reel-layout
description: Aashish's reel workflow on Instagram Edits for Mac. Stage 1 turns a raw talking-head video into his base layout in Edits (tracked cutout over a wooden photo card, black frame, "Save this reel" strip above the head), then stops for his review. Stage 2 polishes the reviewed export with Aashish Cooks using his rules for this layout. Use when Aashish gives a raw video and says "do the layout", "make the cutout", "Edits layout", "wood card", "stage 1", or asks to cook a video that already has this layout.
---

# Aashish reel layout

Aashish is a creator, not a developer. Keep replies short, do the work, never ask him to run commands. He likes terse replies.

Edits is driven through its local MCP server (tools named `mcp__metapilot-native__*`, server "Edits automation"). If the tools fail with connection refused, ask him to open Edits and turn on Settings > Automation > Enable Automation Server.

## Stage 1: base layout in Edits

Goal: one Edits project with this layer stack, bottom to top, all full length, canvas 9:16:

| Layer | What | Transform (x, y = centre, 0-1) |
|---|---|---|
| Main track | Raw video, opacity 0, volume 1 (audio only) | as added |
| Wood card | `assets/wood.jpg` | scale 0.888, x 0.5, y 0.984; rectangle mask, full size, cornerRadius 0.06, feather 0 |
| Cutout | Tracked cutout of Aashish, volume 0 | scale 0.970, x 0.522, y 0.723 |
| Save this reel strip | `assets/save-this-reel.png` (1000x100) | scale 1.093, x 0.513, y 0.483 |

The top of the frame (y 0 to about 0.37) stays black. He adds the title strip (a different one for each reel, like "JOBLESS VIDEO EDITOR", at scale 1.219, x 0.517, y 0.410) and any screen recordings himself after review. Do not add a title strip unless he gives one.

### Steps

1. Copy the raw video and both assets into the Edits sandbox: `~/Library/Containers/com.burbn.basel.mac/Data/tmp/claude/`. Edits cannot read files anywhere else.
2. `newProject`, then `addMedia(path, audioKind: "")` for the raw video. It lands on the main track.
3. **Tracked cutout.** This is the step he cares about most. A plain `addStickerFromCutout` follows him frame by frame but can keep patches of the background (cupboard next to his head, dark wedge by the shoulder). His manual fix in the app is: right-click the clip > Cutout > (click him) > **Track object**. Through the MCP:
   - Tested on 2026-11-07: `trackObject(id: <main clip>, prompt: "person", sampleEvery: 5, saveMasks: true)` tracked all 2006 frames of a 67 s clip in roughly 10 minutes (poll `jobStatus` with the jobId). It writes one mask PNG per frame, named by milliseconds, to `~/Library/Containers/com.burbn.basel.mac/Data/Library/Application Support/sam3-masks/<requestId>/`. The masks were clean at the frames where the plain cutout had leaked. Not yet tested: turning that mask folder into the clip's cutout with `applySubjectEffect(id, storePath, effect)`. Try it once, then check frames.
   - Working default, interactive: make the cutout with `addStickerFromCutout(id)`, check frames every ~1.5 s, and if any edge leaks, stop and ask Aashish: "Right-click the clip > Cutout > Track object, then tell me when it finishes." Wait for him, then check the frames again. He prefers this over guessing.
   - Mute the cutout (`setVolume 0`); keep audio on the main clip.
4. Hide the original picture: `setOpacity(main clip, 0)`.
5. Wood card: `addOverlay(wood.jpg, startSeconds 0, x 0.5, y 0.5, scale 1)`, then `setTransform(id, x 0.5, y 0.984, scale 0.888, allowBeyondCanvas true, keyframes "reject")`, `setMask(id, rectangle, centre 0.5/0.5, size 1/1, cornerRadius 0.06, feather 0)`. Overlays default to 3 s: `trim(id, right, -(duration - 3))` to full length. `moveToLayer` so the wood sits below the cutout.
6. Cutout transform: `setTransform(cutout, x 0.522, y 0.723, scale 0.970, allowBeyondCanvas true, keyframes "reject")`.
7. Save this reel strip: `addOverlay(save-this-reel.png, 0, x 0.513, y 0.483, scale 1.093)`, trim to full length, keep it above the cutout.
8. Check: `captureFrame(times: every ~1.5 s across the clip)` and look at every frame. The cutout must hug him with no cupboard patches or wedges, the head must rise above the wood card, the strip must sit above the head.
9. `saveProject`, `renameProject` to `<video name> layout`.
10. **Stop.** Tell him: the project name, what you checked, anything that looked off. Do not export and do not start Stage 2. He reviews, adds his title strip and recordings, and tells you when to continue.

## Stage 2: Aashish Cooks on this layout

Only after he says to continue.

**Dependency check first.** Stage 2 needs the Aashish Cooks skill. Before anything else, check that it is installed: it appears as `aashish-cooks` in the available skills list, or `~/.claude/skills/aashish-cooks/scripts/cook.py` exists. If it is missing, stop and reply only with:

> Stage 2 needs the Aashish Cooks skill, and it isn't installed. Install it from https://github.com/Aashishb4u/video-skill-aashish-cooks (clone it, then link the folder to `~/.claude/skills/aashish-cooks`), start a new Claude Code session, and ask for stage 2 again. Stage 1 works without it.

Do not try to rebuild Cooks features by hand.

Use the `aashish-cooks` skill, with these rules learned on his reels:

- **Export:** `setExportSettings(dynamicRange SDR, resolution "1080x1920", resolutionType HD, aspectRatio nineBySixteen, quality High)`, then `export` into the sandbox folder. All three of resolutionType, aspectRatio and quality are needed. Output comes out at 60 fps; re-encode to 30 fps with ffmpeg. Trim to the real length (stray clips past the end can make the export much longer).
- **Intro:** if he has an intro clip at the start (about 0 to 3.5 s), add nothing there unless he asks. Start captions after it with a trimmed words file.
- **Transcript:** Hinglish. Whisper on the whole file drops chunks; run `scripts/chunk_words.py` (overlapping ~12 s chunks, `language hi`) and romanize the words by hand, keeping the times. Never use `--lang en`: it translates.
- **Secrets in screen recordings:** find every QR code, login code, access token and API key, including tokens inside screenshots shown in a chat. Pixelate them with ffmpeg (crop, boxblur, overlay with `enable=between(t,a,b)`). Check every frame at the start and end of each window; the first frame of a screen often slips through.
- **Click effects:** a white ripple with a small crimson dot plus the `click` sound, only on 3 to 4 key clicks in the recordings (`scripts/click_ripples.py`, edit the CLICKS list with time, x, y).
- **Cooks plan settings:** `card_y: 92` (keeps cards above the title strip), `captions.bottom: 1160` (pill sits on his chest just under the chin, never on the face, never at the very bottom), `max_words: 3`, `voice: {clean: true, strength: "strong"}`. Cards only in the empty top area, never over recordings. Full-screen booms are fine for 2 to 8 s.
- **Sound:** the text scroll `cooking` sound sits at -5 dB in `sfx.json`. Keep it under his voice.
- **Before handing over:** scan the caption area for single-frame dropouts (should be zero) and look at frames across the whole reel.

## Stage 3 (only when asked)

Reel caption with a "Comment KEYWORD" call to action, a guide written into a copy of his Creative Hand letterhead Google Doc, and a SuperProfile digital product at Rs 49 with a 16:9 banner. Save drafts first and publish only after he says yes.
