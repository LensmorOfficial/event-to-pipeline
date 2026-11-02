#!/usr/bin/env python3
"""Render the README artwork and a 30-second replay from a saved live result.

Requires Pillow (scripts/requirements-assets.txt). The GIF is a result replay,
not a recording of a client session or a claim about query latency.
"""

import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, INK, MUTED, ACCENT = "#0b1220", "#142134", "#f1f5f9", "#a9b9cd", "#74f4c5"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def label(draw, xy, value, size=20, fill=MUTED, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill, spacing=10)


def brand(draw, width):
    draw.rounded_rectangle((48, 38, 64, 54), radius=4, fill=ACCENT)
    label(draw, (76, 30), "LENSMOR / EVENT-TO-PIPELINE", 18, INK, True)
    draw.line((48, 82, width - 48, 82), fill="#26374f", width=1)


def banner(output):
    im = Image.new("RGB", (1280, 640), BG)
    draw = ImageDraw.Draw(im)
    brand(draw, 1280)
    label(draw, (48, 112), "The right companies.", 60, INK, True)
    label(draw, (48, 184), "One focused prompt.", 60, ACCENT, True)
    label(draw, (51, 278), "Live event data + seven Agent Skills for your sales workflow.", 25)
    cards = [("01", "Find events", "Choose your market"), ("02", "Build a shortlist", "See the fit evidence"),
             ("03", "Find people", "Start with relevant roles"), ("04", "Draft outreach", "Make the first message count")]
    for i, (number, title, caption) in enumerate(cards):
        x = 48 + i * 300
        draw.rounded_rectangle((x, 355, x + 284, 524), radius=16, fill=PANEL)
        label(draw, (x + 22, 375), number, 18, ACCENT, True)
        label(draw, (x + 22, 416), title, 25, INK, True)
        label(draw, (x + 22, 465), caption, 17)
    label(draw, (48, 575), "Claude Code   /   Codex   /   Cursor   /   Remote MCP", 20)
    label(draw, (1020, 574), "lensmor.com", 20, ACCENT, True)
    im.save(output / "readme-banner.png", optimize=True)
    im.save(output / "social-preview.png", optimize=True)


def replay(output, data):
    selected = [company for company in data["companies"] if company["qualification"] == "MATCH"]
    company = selected[0]
    event = data["event"]
    frames = []
    scenes = [
        ("01 / ASK", "Start with your target.", ["Find surgical-robotics providers", "at MEDICA 2026."], "A focused requirement, in plain language."),
        ("02 / RESOLVE", event["name"], ["16-19 November 2026", event["venue"] + " / " + event["country"]], "The exact edition becomes the research scope."),
        ("03 / RESEARCH", "Surgical robotics", ["Research provider capabilities", "using Lensmor company records."], "Keep the complete product requirement."),
        ("04 / SELECT", company["name"], [company["hq"], company["employee_size"] + " employees"], "Selected account / returned qualification: MATCH"),
        ("05 / EVIDENCE", "See why it fits.", textwrap.wrap(company["description"], 62)[:4], "Matching evidence: the returned company description."),
        ("06 / NEXT", "A focused account list.", [f"{len(selected)} selected account with matching evidence", "Next: choose a role, then draft an invitation."], "Read the full MEDICA example in the repository."),
    ]
    for index, (step, title, lines, caption) in enumerate(scenes):
        im = Image.new("RGB", (1040, 600), BG)
        draw = ImageDraw.Draw(im)
        brand(draw, 1040)
        label(draw, (48, 108), step, 19, ACCENT, True)
        label(draw, (48, 154), title, 46, INK, True)
        draw.rounded_rectangle((48, 238, 992, 440), radius=18, fill=PANEL)
        for j, line in enumerate(lines):
            label(draw, (72, 262 + j * 37), line, 25, INK)
        label(draw, (48, 460), caption, 19)
        label(draw, (48, 545), "LIVE RESULT REPLAY / " + data["as_of"] + " / MEDICA 2026", 16)
        for j in range(6):
            draw.rounded_rectangle((818 + j * 29, 551, 836 + j * 29, 557), radius=3, fill=ACCENT if j <= index else "#26374f")
        frames.append(im)
    frames[0].save(output / "medica-live-demo.gif", save_all=True, append_images=frames[1:],
                   duration=5000, loop=0, optimize=True)


def main():
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    data = json.loads((ROOT / "examples/04-medica-live/result.json").read_text(encoding="utf-8"))
    banner(output)
    replay(output, data)
    print("Rendered README banner, social preview and 30-second live-result replay.")


if __name__ == "__main__":
    main()
