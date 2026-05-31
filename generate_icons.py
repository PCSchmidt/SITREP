"""
SITREP Icon Generator
Generates all 5 required app store icon assets.
Run from project root: python generate_icons.py
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ── Design tokens ──────────────────────────────────────────────────────────
SIZE = 1024
BLACK        = (0,   0,   0,   255)
BLACK_RGB    = (0,   0,   0)
AMBER        = (255, 165,  0,   255)
AMBER_RGB    = (255, 165,  0)
WHITE        = (255, 255, 255, 255)
WHITE_RGB    = (255, 255, 255)
TRANSPARENT  = (0,   0,   0,   0)

FONT_BOLD   = "C:/Windows/Fonts/arialbd.ttf"
FONT_MONO   = "C:/Windows/Fonts/consolab.ttf"
OUT_DIR     = Path("mobile/assets")


# ── Helpers ─────────────────────────────────────────────────────────────────

def make_canvas(mode="RGB", bg=BLACK_RGB):
    if mode == "RGBA":
        img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    else:
        img = Image.new("RGB", (SIZE, SIZE), bg)
    return img, ImageDraw.Draw(img)


def draw_border(draw, inset=40, thickness=6, color=AMBER_RGB):
    """Thin rectangular border, inset from edges."""
    r = [inset, inset, SIZE - inset, SIZE - inset]
    draw.rectangle(r, outline=color, width=thickness)


def draw_corner_ticks(draw, inset=40, tick=70, thickness=6, color=AMBER_RGB):
    """Military-style corner ticks (like a targeting reticle or document corner)."""
    corners = [
        # top-left
        [(inset, inset + tick), (inset, inset), (inset + tick, inset)],
        # top-right
        [(SIZE - inset - tick, inset), (SIZE - inset, inset), (SIZE - inset, inset + tick)],
        # bottom-left
        [(inset, SIZE - inset - tick), (inset, SIZE - inset), (inset + tick, SIZE - inset)],
        # bottom-right
        [(SIZE - inset - tick, SIZE - inset), (SIZE - inset, SIZE - inset), (SIZE - inset, SIZE - inset - tick)],
    ]
    for pts in corners:
        draw.line(pts, fill=color, width=thickness)


def draw_dividers(draw, y_top, y_bottom, inset=90, color=AMBER_RGB):
    """Thin horizontal lines above and below the main text."""
    draw.line([(inset, y_top), (SIZE - inset, y_top)], fill=color, width=2)
    draw.line([(inset, y_bottom), (SIZE - inset, y_bottom)], fill=color, width=2)


def centred_text(draw, text, font, y_center, color):
    """Draw text horizontally centred at a given y midpoint."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (SIZE - w) / 2 - bbox[0]
    y = y_center - h / 2 - bbox[1]
    draw.text((x, y), text, fill=color, font=font)
    return h


def spaced_text(draw, text, font, y_center, color, spacing=22, max_width=None):
    """Draw text with extra letter spacing, optionally clamped to max_width."""
    char_widths = []
    char_offsets = []  # left-side bearing per character
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=font)
        char_widths.append(bb[2] - bb[0])
        char_offsets.append(bb[0])

    total_width = sum(char_widths) + spacing * (len(text) - 1)

    # Scale down spacing if total exceeds max_width
    if max_width and total_width > max_width:
        available = max_width - sum(char_widths)
        spacing = max(0, available / max(1, len(text) - 1))
        total_width = sum(char_widths) + spacing * (len(text) - 1)

    x = (SIZE - total_width) / 2
    for i, ch in enumerate(text):
        bb = draw.textbbox((0, 0), ch, font=font)
        h = bb[3] - bb[1]
        y = y_center - h / 2 - bb[1]
        draw.text((x - char_offsets[i], y), ch, fill=color, font=font)
        x += char_widths[i] + spacing


# ── Asset 1 & 2: Main icon (RGB) ────────────────────────────────────────────

def build_icon(inset=40, tick=65, border_thickness=5) -> Image.Image:
    """
    Full-colour SITREP icon on black — clean, no disclaimer text.
    Matches the android-icon-foreground aesthetic on a black background.
    """
    img, draw = make_canvas("RGB", BLACK_RGB)

    font_main = ImageFont.truetype(FONT_BOLD, 210)
    font_sub  = ImageFont.truetype(FONT_MONO,  46)

    # Decorative border + corner ticks
    draw_border(draw, inset=inset, thickness=border_thickness, color=AMBER_RGB)
    draw_corner_ticks(draw, inset=inset, tick=tick, thickness=border_thickness, color=AMBER_RGB)

    # Main wordmark — SITREP with extra letter spacing, clamped to safe width
    spaced_text(draw, "SITREP", font_main, 470, AMBER_RGB, spacing=18, max_width=900)

    # Divider lines flanking the wordmark
    draw_dividers(draw, y_top=328, y_bottom=630, inset=90, color=AMBER_RGB)

    # Subtitle
    centred_text(draw, "INTELLIGENCE BRIEFING", font_sub, 730, AMBER_RGB)

    return img


# ── Asset 3: Splash icon (minimal, centred on black) ────────────────────────

def build_splash() -> Image.Image:
    """
    Splash screen icon — matches android-icon-foreground aesthetic on black.
    Clean: no disclaimer text. Displayed centred on the black splash background.
    """
    img, draw = make_canvas("RGB", BLACK_RGB)

    font_main = ImageFont.truetype(FONT_BOLD, 185)
    font_sub  = ImageFont.truetype(FONT_MONO,  50)

    # Thin centre frame with corner ticks
    draw_border(draw, inset=60, thickness=3, color=AMBER_RGB)
    draw_corner_ticks(draw, inset=60, tick=80, thickness=4, color=AMBER_RGB)

    # SITREP — clamped to safe width
    spaced_text(draw, "SITREP", font_main, 460, AMBER_RGB, spacing=24, max_width=860)
    draw_dividers(draw, y_top=345, y_bottom=590, inset=100, color=AMBER_RGB)

    # Subtitle only — no disclaimer
    centred_text(draw, "INTELLIGENCE BRIEFING", font_sub, 680, AMBER_RGB)

    return img


# ── Asset 4: Android adaptive foreground (RGBA, transparent bg) ─────────────

def build_android_foreground() -> Image.Image:
    """
    Android adaptive icon foreground layer — transparent background.
    Key content kept in the inner 66% (safe zone for adaptive masking).
    """
    img, draw = make_canvas("RGBA")

    font_main = ImageFont.truetype(FONT_BOLD, 155)
    font_sub  = ImageFont.truetype(FONT_MONO,  38)

    # Safe zone = inset ~170px each side (66% of 1024 = 676px centred)
    safe_inset = 170
    safe_width = SIZE - 2 * safe_inset  # 684px usable

    draw_border(draw, inset=safe_inset, thickness=5, color=AMBER)
    draw_corner_ticks(draw, inset=safe_inset, tick=55, thickness=5, color=AMBER)

    centred_text(draw, "UNCLASSIFIED", font_sub, 266, AMBER)
    spaced_text(draw, "SITREP", font_main, 490, AMBER, spacing=14, max_width=safe_width - 40)
    draw_dividers(draw, y_top=380, y_bottom=614, inset=210, color=AMBER)
    centred_text(draw, "INTEL BRIEF", font_sub, 718, AMBER)

    return img


# ── Asset 5: Android monochrome (white silhouette, transparent bg) ───────────

def build_android_monochrome() -> Image.Image:
    """
    Android themed icon — white silhouette on transparent background.
    Used when the user has a coloured wallpaper theme.
    """
    img, draw = make_canvas("RGBA")

    font_main = ImageFont.truetype(FONT_BOLD, 200)
    font_sub  = ImageFont.truetype(FONT_MONO,  50)

    safe_inset = 160
    draw_border(draw, inset=safe_inset, thickness=5, color=WHITE)
    draw_corner_ticks(draw, inset=safe_inset, tick=60, thickness=5, color=WHITE)
    spaced_text(draw, "SITREP", font_main, 490, WHITE, spacing=16)
    draw_dividers(draw, y_top=360, y_bottom=636, inset=200, color=WHITE)
    centred_text(draw, "INTELLIGENCE", font_sub, 720, WHITE)

    return img


# ── Asset 6: Android background (solid black) ───────────────────────────────

def build_android_background() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), BLACK_RGB)
    return img


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    assets = [
        ("icon.png",                      build_icon()),
        ("splash-icon.png",               build_splash()),
        ("android-icon-foreground.png",   build_android_foreground()),
        ("android-icon-monochrome.png",   build_android_monochrome()),
        ("android-icon-background.png",   build_android_background()),
    ]

    for filename, img in assets:
        path = OUT_DIR / filename
        # Convert RGBA → RGB for files that don't support transparency
        if filename in ("icon.png", "splash-icon.png", "android-icon-background.png"):
            if img.mode == "RGBA":
                bg = Image.new("RGB", img.size, BLACK_RGB)
                bg.paste(img, mask=img.split()[3])
                img = bg
        img.save(path, "PNG", optimize=False)
        size_kb = path.stat().st_size / 1024
        w, h = img.size
        print(f"  {filename}: {w}x{h}  ({size_kb:.0f} KB)")

    print(f"\nAll 5 assets written to {OUT_DIR}/")
    print("Open mobile/assets/ in your file explorer to preview.")


if __name__ == "__main__":
    print("Generating SITREP icon assets...\n")
    main()
