# Executive Intelligence Briefing PDF Generator v3
# Editorial / executive design: serif headlines (PT Serif) + clean sans body
# (Lato), restrained navy palette with hairline rules, two-column cover
# (Contents + Executive Summary), numbered thematic sections, and hyperlinked
# per-section references. Falls back to base-14 fonts if the bundled TTFs are
# unavailable, so it never hard-fails on a fresh environment.

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, List, Union

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable, FrameBreak, NextPageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

logger = logging.getLogger(__name__)

_FONT_DIR = Path(__file__).parent / "fonts"


class PDFGeneratorV3:
    """Executive-grade PDF generator for intelligence briefings."""

    # Restrained editorial palette
    NAVY = HexColor('#13233b')      # headlines, masthead
    INK = HexColor('#1c2330')       # body text
    SLATE = HexColor('#5b6675')     # secondary / labels
    HAIRLINE = HexColor('#c5ccd4')  # thin rules
    FAINT = HexColor('#eef1f5')     # subtle fills
    LINK = HexColor('#1d4e89')      # restrained link blue
    WHITE = HexColor('#ffffff')

    def __init__(self):
        self.SERIF, self.SANS = self._register_fonts()
        self._setup_styles()

    # ---- fonts -------------------------------------------------------------
    def _register_fonts(self):
        """Register bundled TTFs; return (serif_family, sans_family) names.

        Falls back to Times/Helvetica if the TTFs aren't present so the
        generator works on any environment.
        """
        try:
            specs = {
                'PTSerif': 'PTSerif-Regular.ttf',
                'PTSerif-Bold': 'PTSerif-Bold.ttf',
                'PTSerif-Italic': 'PTSerif-Italic.ttf',
                'PTSerif-BoldItalic': 'PTSerif-BoldItalic.ttf',
                'Lato': 'Lato-Regular.ttf',
                'Lato-Bold': 'Lato-Bold.ttf',
                'Lato-Italic': 'Lato-Italic.ttf',
                'Lato-BoldItalic': 'Lato-BoldItalic.ttf',
            }
            for name, fname in specs.items():
                path = _FONT_DIR / fname
                if not path.exists():
                    raise FileNotFoundError(path)
                pdfmetrics.registerFont(TTFont(name, str(path)))
            pdfmetrics.registerFontFamily(
                'PTSerif', normal='PTSerif', bold='PTSerif-Bold',
                italic='PTSerif-Italic', boldItalic='PTSerif-BoldItalic')
            pdfmetrics.registerFontFamily(
                'Lato', normal='Lato', bold='Lato-Bold',
                italic='Lato-Italic', boldItalic='Lato-BoldItalic')
            logger.info("PDFv3: registered PT Serif + Lato")
            return 'PTSerif', 'Lato'
        except Exception as e:
            logger.warning(f"PDFv3: bundled fonts unavailable ({e}); using base-14 fallback")
            return 'Times-Roman', 'Helvetica'

    # ---- styles ------------------------------------------------------------
    def _setup_styles(self):
        S, N = self.SERIF, self.SANS
        self.st = {}
        add = lambda **kw: self.st.__setitem__(kw['name'], ParagraphStyle(**kw))

        add(name='Masthead', fontName=S, fontSize=42, textColor=self.NAVY,
            alignment=TA_CENTER, leading=46, spaceAfter=0)
        add(name='Tagline', fontName=N, fontSize=8.5, textColor=self.SLATE,
            alignment=TA_CENTER, leading=12, spaceAfter=0)
        add(name='Cutoff', fontName=N, fontSize=9, textColor=self.NAVY,
            alignment=TA_CENTER, leading=13)
        add(name='Disclaimer', fontName=N, fontSize=8.5, textColor=self.SLATE,
            alignment=TA_CENTER, leading=12.5)
        add(name='RegionCover', fontName=S, fontSize=23, textColor=self.NAVY,
            alignment=TA_CENTER, leading=27, spaceAfter=2)
        add(name='DateCover', fontName=N, fontSize=10.5, textColor=self.SLATE,
            alignment=TA_CENTER, leading=14)

        add(name='ColHead', fontName=N, fontSize=9.5, textColor=self.NAVY,
            alignment=TA_LEFT, leading=13, spaceAfter=8)
        add(name='ContentsItem', fontName=N, fontSize=10.5, textColor=self.INK,
            alignment=TA_LEFT, leading=20)
        add(name='ContentsSub', fontName=N, fontSize=8.5, textColor=self.SLATE,
            alignment=TA_LEFT, leading=12)
        add(name='ExecBody', fontName=S, fontSize=10.5, textColor=self.INK,
            alignment=TA_JUSTIFY, leading=15.5)

        add(name='RegionHead', fontName=S, fontSize=22, textColor=self.NAVY,
            alignment=TA_LEFT, leading=26, spaceAfter=2)
        add(name='BlufLabel', fontName=N, fontSize=8.5, textColor=self.NAVY,
            alignment=TA_LEFT, leading=12, spaceAfter=3)
        add(name='BlufBody', fontName=S, fontSize=11, textColor=self.INK,
            alignment=TA_JUSTIFY, leading=16)
        add(name='SectionHead', fontName=S, fontSize=14, textColor=self.NAVY,
            alignment=TA_LEFT, leading=18, spaceBefore=14, spaceAfter=5)
        add(name='Label', fontName=N, fontSize=9, textColor=self.NAVY,
            alignment=TA_LEFT, leading=13, spaceBefore=10, spaceAfter=5)
        add(name='Body', fontName=N, fontSize=10, textColor=self.INK,
            alignment=TA_JUSTIFY, leading=15)
        add(name='Bullet', fontName=N, fontSize=10, textColor=self.INK,
            alignment=TA_LEFT, leading=14.5, leftIndent=14, bulletIndent=2)
        add(name='SrcLabel', fontName=N, fontSize=8, textColor=self.SLATE,
            alignment=TA_LEFT, leading=11, spaceBefore=4)
        add(name='Source', fontName=N, fontSize=8.5, textColor=self.INK,
            alignment=TA_LEFT, leading=12.5, leftIndent=12, bulletIndent=0)

    # ---- helpers -----------------------------------------------------------
    # Repairs for UTF-8 punctuation mis-decoded as Windows-1252 (mojibake).
    # Keys are the broken sequences; ordered most-specific first so the bare
    # 'â€' catch-all (right double quote) runs last. Only triggers on already-
    # broken text, so it is a no-op on correctly-encoded content.
    _MOJIBAKE = [
        ('â€™', '’'), ('â€˜', '‘'),
        ('â€œ', '“'), ('â€\x9d', '”'),
        ('â€”', '—'), ('â€“', '–'),
        ('â€¦', '…'),
        ('Ã©', 'é'), ('Ã¨', 'è'), ('Ã±', 'ñ'),
        ('Â\xa0', ' '), ('Â ', ' '),
        ('â€', '”'),
    ]

    @classmethod
    def _fix_text(cls, text: str) -> str:
        if not text or 'Ã' not in text and 'â' not in text and 'Â' not in text:
            return text or ''
        for bad, good in cls._MOJIBAKE:
            if bad in text:
                text = text.replace(bad, good)
        return text

    @classmethod
    def _esc(cls, text: str) -> str:
        text = cls._fix_text(text or '')
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return text

    def _spaced_caps(self, text: str, gap: str = ' ') -> str:
        """Letter-spaced caps for masthead tagline / labels."""
        return gap.join(list(text.upper()))

    def _fmt_cutoff(self, briefing: Dict) -> str:
        gen = briefing.get('generated_at', '')
        try:
            dt = datetime.fromisoformat(gen.replace('Z', '+00:00'))
        except Exception:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%H%MZ / %d %b %Y").upper()

    def _fmt_date(self, briefing: Dict) -> str:
        gen = briefing.get('generated_at', '')
        try:
            dt = datetime.fromisoformat(gen.replace('Z', '+00:00'))
        except Exception:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%d %b %Y").upper()

    # ---- public ------------------------------------------------------------
    def generate_pdf(self, briefing: Dict, output_path: Optional[str] = None) -> str:
        region = briefing.get('region', 'Global')
        logger.info(f"PDFv3: generating {region} briefing")

        if not output_path:
            output_dir = Path("data/pdfs")
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.utcnow().strftime("%Y-%m-%d")
            slug = region.lower().replace(' ', '_').replace('/', '_')
            output_path = output_dir / f"{slug}_{timestamp}.pdf"

        self._region = region
        self._date_str = self._fmt_date(briefing)

        doc = BaseDocTemplate(
            str(output_path), pagesize=letter,
            leftMargin=0.85 * inch, rightMargin=0.85 * inch,
            topMargin=0.8 * inch, bottomMargin=0.75 * inch,
            title=f"SITREP — {region} Intelligence Briefing",
            author="SITREP",
        )
        width, height = letter
        fl, fr = doc.leftMargin, doc.rightMargin
        fw = width - fl - fr
        body_frame = Frame(fl, doc.bottomMargin, fw,
                           height - doc.topMargin - doc.bottomMargin, id='body')
        cover_frame = Frame(fl, doc.bottomMargin, fw,
                            height - doc.topMargin - doc.bottomMargin, id='cover')
        doc.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame], onPage=self._cover_canvas),
            PageTemplate(id='content', frames=[body_frame], onPage=self._content_canvas),
        ])

        story = [NextPageTemplate('content')]
        story += self._build_cover(briefing, fw)
        story.append(PageBreak())
        story += self._build_content(briefing)

        doc.build(story)
        size_kb = Path(output_path).stat().st_size / 1024
        logger.info(f"PDFv3: wrote {output_path} ({size_kb:.1f} KB)")
        return str(output_path)

    # ---- page furniture ----------------------------------------------------
    def _cover_canvas(self, canvas, doc):
        canvas.saveState()
        width, height = doc.pagesize
        canvas.setFillColor(self.SLATE)
        canvas.setFont(self.SANS, 7)
        canvas.drawCentredString(
            width / 2, 0.5 * inch,
            "AI-GENERATED OPEN-SOURCE SUMMARY  •  NOT OFFICIAL INTELLIGENCE  •  ACCURACY NOT GUARANTEED")
        canvas.restoreState()

    def _content_canvas(self, canvas, doc):
        canvas.saveState()
        width, height = doc.pagesize
        lm, rm = doc.leftMargin, width - doc.rightMargin
        # Running header
        canvas.setFillColor(self.NAVY)
        canvas.setFont(self.SANS, 7.5)
        canvas.drawString(lm, height - 0.5 * inch,
                          self._spaced_caps("SITREP"))
        canvas.setFillColor(self.SLATE)
        canvas.drawRightString(rm, height - 0.5 * inch,
                               f"{self._region.upper()}  •  {self._date_str}")
        canvas.setStrokeColor(self.HAIRLINE)
        canvas.setLineWidth(0.5)
        canvas.line(lm, height - 0.58 * inch, rm, height - 0.58 * inch)
        # Footer
        canvas.setStrokeColor(self.HAIRLINE)
        canvas.line(lm, 0.62 * inch, rm, 0.62 * inch)
        canvas.setFont(self.SANS, 7)
        canvas.setFillColor(self.SLATE)
        canvas.drawString(lm, 0.46 * inch, "SITREP")
        canvas.drawCentredString(width / 2, 0.46 * inch,
                                 "AI-GENERATED  •  NOT FOR OPERATIONAL USE")
        canvas.drawRightString(rm, 0.46 * inch, f"{self._date_str}  •  PAGE {doc.page}")
        canvas.restoreState()

    def _rule(self, width_pts, thickness=0.75, color=None, space_before=0, space_after=0):
        # width_pts None -> full frame width ("100%"); HRFlowable rejects None.
        w = "100%" if width_pts is None else width_pts
        return HRFlowable(width=w, thickness=thickness,
                          color=color or self.HAIRLINE, lineCap='butt',
                          spaceBefore=space_before, spaceAfter=space_after)

    # ---- cover -------------------------------------------------------------
    def _build_cover(self, briefing: Dict, fw) -> List:
        e = []
        e.append(Spacer(1, 0.35 * inch))
        e.append(Paragraph("SITREP", self.st['Masthead']))
        e.append(Spacer(1, 4))
        e.append(self._rule(fw, thickness=1.5, color=self.NAVY, space_after=4))
        e.append(Paragraph(self._spaced_caps("AI-Generated Open-Source Intelligence Summary"),
                           self.st['Tagline']))
        e.append(self._rule(fw, thickness=0.75, color=self.NAVY, space_before=4, space_after=18))

        # Region + cutoff
        e.append(Paragraph(self._esc(briefing.get('region', 'Global')), self.st['RegionCover']))
        e.append(Paragraph(f"Information Cutoff: {self._fmt_cutoff(briefing)}", self.st['DateCover']))
        e.append(Spacer(1, 16))

        # Disclaimer band
        disc = Paragraph(
            "This product is an AI-generated synthesis of open-source reporting, provided for general "
            "informational awareness only. It is not official intelligence, and accuracy is not guaranteed. "
            "Views belong to the cited authors. Do not use for operational decision-making.",
            self.st['Disclaimer'])
        band = Table([[disc]], colWidths=[fw])
        band.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.FAINT),
            ('LINEABOVE', (0, 0), (-1, -1), 2, self.NAVY),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, self.HAIRLINE),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 22),
            ('RIGHTPADDING', (0, 0), (-1, -1), 22),
        ]))
        e.append(band)
        e.append(Spacer(1, 22))

        # Two-column: Contents | Executive Summary
        contents_cell = [Paragraph(self._spaced_caps("Contents"), self.st['ColHead'])]
        regions = briefing.get('regions')
        if isinstance(regions, list) and regions:
            # Composite Global: list the regions covered, each in full.
            for i, sub in enumerate(regions, 1):
                contents_cell.append(Paragraph(
                    f"{i}.&nbsp;&nbsp;{self._esc(sub.get('region', 'Region'))}",
                    self.st['ContentsItem']))
        else:
            sections = briefing.get('sections', [])
            if sections:
                for i, sec in enumerate(sections, 1):
                    contents_cell.append(Paragraph(
                        f"{i}.&nbsp;&nbsp;{self._esc(sec.get('title', 'Untitled'))}",
                        self.st['ContentsItem']))
            else:
                contents_cell.append(Paragraph("Full briefing", self.st['ContentsItem']))
            contents_cell.append(Spacer(1, 10))
            contents_cell.append(Paragraph("Outlook", self.st['ContentsItem']))
            contents_cell.append(Paragraph("References & Sourcing", self.st['ContentsItem']))

        exec_cell = [Paragraph(self._spaced_caps("Executive Summary"), self.st['ColHead'])]
        bluf = self._esc(briefing.get('bluf', 'No summary available.'))
        exec_cell.append(Paragraph(bluf, self.st['ExecBody']))

        col_gap = 0.35 * inch
        left_w = fw * 0.34
        right_w = fw - left_w - col_gap
        cols = Table([[contents_cell, '', exec_cell]],
                     colWidths=[left_w, col_gap, right_w])
        cols.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEAFTER', (0, 0), (0, 0), 0.5, self.HAIRLINE),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), col_gap / 2),
            ('LEFTPADDING', (2, 0), (2, 0), col_gap / 2),
        ]))
        e.append(cols)
        return e

    # ---- content -----------------------------------------------------------
    def _build_content(self, briefing: Dict) -> List:
        """Dispatch single-region vs composite (Global = 4 regions in full)."""
        regions = briefing.get('regions')
        if isinstance(regions, list) and regions:
            e = []
            for i, sub in enumerate(regions):
                if i > 0:
                    e.append(PageBreak())
                e.extend(self._render_region_block(sub))
            return e
        return self._render_region_block(briefing)

    def _render_region_block(self, briefing: Dict) -> List:
        e = []
        # Region header
        e.append(Paragraph(self._esc(briefing.get('region', 'Global')), self.st['RegionHead']))
        e.append(self._rule(None, thickness=1.2, color=self.NAVY, space_before=2, space_after=10))

        # BLUF lead
        e.append(Paragraph(self._spaced_caps("Bottom Line Up Front"), self.st['BlufLabel']))
        e.append(Paragraph(self._esc(briefing.get('bluf', '')), self.st['BlufBody']))
        e.append(Spacer(1, 6))

        # Key developments
        kds = briefing.get('key_developments') or []
        if kds:
            e.append(Paragraph(self._spaced_caps("Key Developments"), self.st['Label']))
            for kd in kds:
                e.append(Paragraph(self._esc(kd), self.st['Bullet'], bulletText='—'))
            e.append(Spacer(1, 4))

        # Thematic sections
        for i, sec in enumerate(briefing.get('sections', []), 1):
            grp = [self._rule(None, thickness=0.5, color=self.HAIRLINE, space_before=8, space_after=6)]
            grp.append(Paragraph(f"{i}.&nbsp;&nbsp;{self._esc(sec.get('title', 'Untitled'))}",
                                 self.st['SectionHead']))
            body = self._esc(sec.get('content', ''))
            grp.append(Paragraph(body, self.st['Body']))
            srcs = sec.get('sources') or []
            if srcs:
                grp.append(Paragraph(self._spaced_caps("Sources"), self.st['SrcLabel']))
                for j, s in enumerate(srcs, 1):
                    grp.append(Paragraph(self._format_source(s, j), self.st['Source'],
                                         bulletText=''))
            # keep the header with at least its first lines together
            e.append(KeepTogether(grp[:3]))
            e.extend(grp[3:])

        # Outlook
        if briefing.get('outlook'):
            e.append(self._rule(None, thickness=0.5, color=self.HAIRLINE, space_before=8, space_after=6))
            e.append(Paragraph(self._spaced_caps("Outlook"), self.st['Label']))
            e.append(Paragraph(self._esc(briefing.get('outlook', '')), self.st['Body']))

        return e

    def _format_source(self, source: Union[str, Dict], idx: int) -> str:
        if isinstance(source, dict):
            name = self._esc(source.get('source', 'Source'))
            title = self._esc(source.get('title', 'Untitled'))
            url = source.get('url', '') or ''
            label = f"<b>{name}</b> &mdash; {title}"
            if url:
                safe = url.replace('"', '%22')
                return f'{idx}.&nbsp; <link href="{safe}" color="#1d4e89">{label}</link>'
            return f'{idx}.&nbsp; {label}'
        return f'{idx}.&nbsp; {self._esc(str(source))}'


# Backwards-compatible alias so callers can swap generators by import name.
PDFGenerator = PDFGeneratorV3


def _test():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        cand = sorted(Path("data/briefings").glob("*.json"), key=lambda p: p.stat().st_mtime)
        path = str(cand[-1]) if cand else None
    if not path:
        print("no briefing json found"); return
    with open(path, 'r', encoding='utf-8') as f:
        briefing = json.load(f)
    out = PDFGeneratorV3().generate_pdf(briefing, output_path="test_v3.pdf")
    print("wrote", out)


if __name__ == "__main__":
    _test()
