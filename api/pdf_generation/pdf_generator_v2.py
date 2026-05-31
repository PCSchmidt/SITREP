# Professional Intelligence Briefing PDF Generator v2
# Clean, modern design with proper spacing and clickable source links

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Union

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

logger = logging.getLogger(__name__)


class PDFGeneratorV2:
    """
    Professional PDF generator for intelligence briefings.

    Design principles:
    - Clean layout with ample whitespace
    - No overlapping text
    - Properly aligned elements
    - Clickable source hyperlinks
    - Professional typography
    """

    # Clean, professional color palette
    NAVY_BLUE = HexColor('#1a3a52')
    STEEL_BLUE = HexColor('#4682b4')
    DARK_TEXT = HexColor('#1a1a1a')
    MED_GRAY = HexColor('#666666')
    LIGHT_GRAY = HexColor('#cccccc')
    ULTRA_LIGHT = HexColor('#f5f5f5')
    ACCENT_ORANGE = HexColor('#e67e22')
    WHITE = HexColor('#ffffff')

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Create clean, professional paragraph styles"""

        # Cover page title
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            fontSize=48,
            textColor=self.NAVY_BLUE,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=20,
            leading=56
        ))

        # Cover subtitle
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            fontSize=18,
            textColor=self.MED_GRAY,
            alignment=TA_CENTER,
            fontName='Helvetica',
            spaceAfter=30,
            leading=22
        ))

        # Cover date/region
        self.styles.add(ParagraphStyle(
            name='CoverMeta',
            fontSize=14,
            textColor=self.DARK_TEXT,
            alignment=TA_CENTER,
            fontName='Helvetica',
            spaceAfter=12,
            leading=18
        ))

        # Section headers
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            fontSize=14,
            textColor=self.NAVY_BLUE,
            fontName='Helvetica-Bold',
            spaceAfter=12,
            spaceBefore=20,
            leading=18,
            borderPadding=0
        ))

        # BLUF box content
        self.styles.add(ParagraphStyle(
            name='BLUFText',
            fontSize=11,
            textColor=self.DARK_TEXT,
            fontName='Helvetica-Bold',
            alignment=TA_JUSTIFY,
            leading=16,
            leftIndent=0,
            rightIndent=0
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='AnalysisBody',
            fontSize=10,
            textColor=self.DARK_TEXT,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            leading=14,
            spaceBefore=0,
            spaceAfter=0
        ))

        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletText',
            fontSize=10,
            textColor=self.DARK_TEXT,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            leading=14,
            leftIndent=20,
            bulletIndent=5
        ))

        # Source links (smaller, with color for links)
        self.styles.add(ParagraphStyle(
            name='SourceLink',
            fontSize=9,
            textColor=self.STEEL_BLUE,
            fontName='Helvetica',
            leading=13,
            leftIndent=20
        ))

        # Footer/disclaimer text
        self.styles.add(ParagraphStyle(
            name='DisclaimerText',
            fontSize=9,
            textColor=self.MED_GRAY,
            fontName='Helvetica',
            alignment=TA_CENTER,
            leading=12
        ))

    def generate_pdf(self, briefing: Dict, output_path: Optional[str] = None) -> str:
        """
        Generate professional PDF from briefing data.

        Args:
            briefing: Briefing dictionary from synthesis
            output_path: Optional custom output path

        Returns:
            Path to generated PDF
        """
        logger.info(f"Generating PDF for {briefing.get('region', 'Unknown')} briefing")

        # Setup output path
        if not output_path:
            output_dir = Path("data/pdfs")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y-%m-%d")
            region_slug = briefing['region'].lower().replace(' ', '_').replace('/', '_')
            output_path = output_dir / f"{region_slug}_{timestamp}.pdf"

        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )

        # Build story
        story = []
        story.extend(self._build_cover(briefing))
        story.append(PageBreak())
        story.extend(self._build_content(briefing))

        # Generate
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        size_kb = Path(output_path).stat().st_size / 1024
        logger.info(f"PDF generated: {output_path} ({size_kb:.1f} KB)")
        return str(output_path)

    def _header_footer(self, canvas, doc):
        """Draw header and footer on each page"""
        canvas.saveState()
        width, height = doc.pagesize

        # Top line
        canvas.setStrokeColor(self.NAVY_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(0.5*inch, height - 0.4*inch, width - 0.5*inch, height - 0.4*inch)

        # Bottom disclaimer
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(self.MED_GRAY)
        canvas.drawCentredString(
            width / 2,
            0.4*inch,
            "AI-GENERATED INTELLIGENCE SUMMARY  •  NOT FOR OPERATIONAL USE  •  ACCURACY NOT GUARANTEED"
        )

        # Page number
        canvas.setFont('Helvetica', 8)
        canvas.drawCentredString(width / 2, 0.25*inch, f"Page {doc.page}")

        canvas.restoreState()

    def _build_cover(self, briefing: Dict) -> List:
        """Build clean cover page"""
        elements = []

        # Vertical spacing
        elements.append(Spacer(1, 2*inch))

        # Title
        elements.append(Paragraph("SITREP", self.styles['CoverTitle']))

        # Subtitle
        elements.append(Paragraph(
            "Intelligence Briefing",
            self.styles['CoverSubtitle']
        ))

        elements.append(Spacer(1, 0.8*inch))

        # Region
        region = briefing.get('region', 'Unknown Region')
        elements.append(Paragraph(f"<b>{region}</b>", self.styles['CoverMeta']))

        # Date
        generated_at = briefing.get('generated_at', datetime.utcnow().isoformat())
        try:
            gen_date = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            date_str = gen_date.strftime("%B %d, %Y")
        except:
            date_str = datetime.utcnow().strftime("%B %d, %Y")

        elements.append(Paragraph(date_str, self.styles['CoverMeta']))

        elements.append(Spacer(1, 1.5*inch))

        # Clean disclaimer box (no borders, just gray background)
        disclaimer_title = Paragraph(
            "<b>AI-GENERATED CONTENT</b>",
            self.styles['CoverMeta']
        )

        disclaimer_body = Paragraph(
            "This briefing synthesizes open-source intelligence using artificial intelligence. "
            "Content accuracy is not guaranteed and should not be used for operational decision-making. "
            "Sources are cited for reference and verification.",
            self.styles['DisclaimerText']
        )

        # Use nested table for proper alignment
        disclaimer_content = [[disclaimer_title], [Spacer(1, 8)], [disclaimer_body]]
        disclaimer_inner = Table(disclaimer_content, colWidths=[5.1*inch])
        disclaimer_inner.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        disclaimer_table = Table(
            [[disclaimer_inner]],
            colWidths=[5.5*inch]
        )
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.ULTRA_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(disclaimer_table)

        return elements

    def _build_content(self, briefing: Dict) -> List:
        """Build main briefing content"""
        elements = []

        # === BLUF ===
        elements.append(Paragraph("BLUF (BOTTOM LINE UP FRONT)", self.styles['SectionTitle']))
        elements.append(Spacer(1, 8))

        # BLUF in clean box with left border accent
        bluf_text = briefing.get('bluf', '')
        bluf_para = Paragraph(bluf_text, self.styles['BLUFText'])

        bluf_table = Table([[bluf_para]], colWidths=[6.5*inch])
        bluf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.ULTRA_LIGHT),
            ('LINEBELOW', (0, 0), (-1, -1), 3, self.ACCENT_ORANGE),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(bluf_table)
        elements.append(Spacer(1, 20))

        # === KEY DEVELOPMENTS ===
        if briefing.get('key_developments'):
            elements.append(Paragraph("KEY DEVELOPMENTS", self.styles['SectionTitle']))
            elements.append(Spacer(1, 8))

            for dev in briefing['key_developments']:
                bullet = Paragraph(f"• {dev}", self.styles['BulletText'])
                elements.append(bullet)
                elements.append(Spacer(1, 6))

            elements.append(Spacer(1, 20))

        # === DETAILED ANALYSIS SECTIONS ===
        for section in briefing.get('sections', []):
            section_group = []

            # Section title
            section_group.append(Paragraph(
                section['title'].upper(),
                self.styles['SectionTitle']
            ))
            section_group.append(Spacer(1, 8))

            # Section content
            content = Paragraph(section['content'], self.styles['AnalysisBody'])
            section_group.append(content)
            section_group.append(Spacer(1, 12))

            # Sources with clickable links
            if section.get('sources'):
                sources_title = Paragraph("<b>Sources:</b>", self.styles['AnalysisBody'])
                section_group.append(sources_title)
                section_group.append(Spacer(1, 4))

                for source in section['sources']:
                    source_text = self._format_source_link(source)
                    source_para = Paragraph(source_text, self.styles['SourceLink'])
                    section_group.append(source_para)
                    section_group.append(Spacer(1, 2))

                section_group.append(Spacer(1, 12))

            # Keep section together
            elements.append(KeepTogether(section_group))

        # === OUTLOOK ===
        if briefing.get('outlook'):
            elements.append(Paragraph("OUTLOOK", self.styles['SectionTitle']))
            elements.append(Spacer(1, 8))

            outlook = Paragraph(briefing['outlook'], self.styles['AnalysisBody'])
            elements.append(outlook)

        return elements

    def _format_source_link(self, source: Union[str, Dict]) -> str:
        """
        Format source with clickable hyperlink.

        Returns formatted HTML with link if URL available.
        """
        if isinstance(source, dict):
            source_name = source.get('source', 'Unknown')
            title = source.get('title', 'Untitled')
            url = source.get('url', '')

            if url:
                # Create clickable link
                return f'• <link href="{url}" color="blue"><b>{source_name}</b>: {title}</link>'
            else:
                # No URL, just format nicely
                return f'• <b>{source_name}</b>: {title}'
        else:
            # Old string format
            return f'• {str(source)}'

    def _clean_text(self, text: str) -> str:
        """Clean text for PDF rendering"""
        # Escape XML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text


# Test function
def test_pdf_v2():
    """Test new PDF generator"""
    # Load a recent briefing
    briefing_path = Path("data/briefings").glob("middle_east_*.json")
    briefing_path = max(briefing_path, key=lambda p: p.stat().st_mtime, default=None)

    if not briefing_path:
        print("No briefings found for testing")
        return

    with open(briefing_path, 'r', encoding='utf-8') as f:
        briefing = json.load(f)

    # Generate PDF
    generator = PDFGeneratorV2()
    pdf_path = generator.generate_pdf(briefing, output_path="test_v2.pdf")

    print(f"Generated: {pdf_path}")
    print(f"Size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    test_pdf_v2()
