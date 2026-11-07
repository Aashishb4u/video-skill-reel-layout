# video-skill-reel-layout

A Claude Code skill for building Aashish's talking-head reel layout in Instagram Edits for Mac, then polishing it with the [Aashish Cooks](https://github.com/Aashishb4u/video-skill-aashish-cooks) skill.

## What it does

**Stage 1, layout in Edits.** From a raw vertical video, the skill builds one Edits project:

- a tracked cutout of the speaker,
- a wooden photo card behind the speaker with rounded top corners,
- a black frame with the top area left free for visuals,
- the "Save this reel" strip above the speaker's head.

It checks frames across the clip, saves the project and stops so the creator can review it and add a title strip and screen recordings.

**Stage 2, Aashish Cooks.** After review, the exported video gets captions, cards, sound effects and voice cleaning with rules tuned for this layout: captions on the chest, cards above the title strip, secrets in screen recordings pixelated, click ripples on a few key clicks.

**Stage 3, optional.** Reel caption, a guide document and a digital product listing.

## Requirements

- macOS with Instagram Edits for Mac, automation server enabled (Settings > Automation > Enable Automation Server)
- Claude Code connected to the Edits MCP server (copy the Claude Code command from the Automation page)
- ffmpeg, and the Aashish Cooks skill for stage 2

## Install

```bash
git clone https://github.com/Aashishb4u/video-skill-reel-layout.git
```

```bash
ln -s "$(pwd)/video-skill-reel-layout" ~/.claude/skills/aashish-reel-layout
```

Then give Claude a raw video and ask for the layout.

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | The skill instructions |
| `assets/save-this-reel.png` | The "Save this reel" strip (1000x100) |
| `assets/wood.jpg` | The wooden card photo (1500x2000) |
| `scripts/click_ripples.py` | Draws click ripples on chosen clicks in screen recordings |
| `scripts/chunk_words.py` | Transcribes Hinglish audio in overlapping chunks so no words are dropped |

## Notes

Unofficial. Not affiliated with Meta, Instagram or Anthropic. The Edits automation server is not publicly documented and can change with app updates.
