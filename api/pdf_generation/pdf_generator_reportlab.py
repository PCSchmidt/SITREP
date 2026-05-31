# Professional PDF Generator using ReportLab
# Generates military-style intelligence briefings with proper formatting

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Union

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generates professional intelligence briefings in PDF format.

    Features:
    - Military-grade professional styling
    - Proper source attribution with publication names
    - Structured sections with clear hierarchy
    - Comprehensive disclaimers and headers
    - Page numbers and footers
    """

    # Professional color palette
    AMBER = HexColor('#FFA500')
    DARK_AMBER = HexColor('#CC8400')
    TRUE_BLACK = HexColor('#000000')
    DARK_GRAY = HexColor('#333333')
    MED_GRAY = HexColor('#666666')
    LIGHT_GRAY = HexColor('#999999')
    VERY_LIGHT_GRAY = HexColor('#f8f8f8')
    WARNING_BG = HexColor('#FFF3CD')
    WARNING_BORDER = HexColor('#856404')
    CLASSIFICATION_RED = HexColor('#8B0000')

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create professional paragraph styles matching intelligence briefing standards"""

        # Cover page: Main title
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Title'],
            fontSize=56,
            textColor=self.TRUE_BLACK,
            alignment=TA_CENTER,
            spaceAfter=6,
            spaceBefore=0,
            fontName='Helvetica-Bold',
            letterSpacing=2
        ))

        # Cover page: Subtitle
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            fontSize=22,
            textColor=self.DARK_GRAY,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica'
        ))

        # Cover page: Region name
        self.styles.add(ParagraphStyle(
            name='CoverRegion',
            fontSize=20,
            textColor=self.TRUE_BLACK,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))

        # Cover page: Date
        self.styles.add(ParagraphStyle(
            name='CoverDate',
            fontSize=13,
            textColor=self.MED_GRAY,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        ))

        # Classification marking
        self.styles.add(ParagraphStyle(
            name='Classification',
            fontSize=11,
            textColor=self.CLASSIFICATION_RED,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=12
        ))

        # Section headers (BLUF, KEY DEVELOPMENTS, etc.)
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=14,
            textColor=self.TRUE_BLACK,
            spaceAfter=10,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            leftIndent=0,
            borderWidth=0,
            borderPadding=0,
            borderColor=None
        ))

        # BLUF content box
        self.styles.add(ParagraphStyle(
            name='BLUFContent',
            fontSize=11,
            leading=17,
            alignment=TA_JUSTIFY,
            leftIndent=15,
            rightIndent=15,
            fontName='Helvetica-Bold',
            textColor=self.TRUE_BLACK
        ))

        # Body text - justified
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0,
            fontName='Helvetica',
            textColor=self.TRUE_BLACK
        ))

        # Bullet points (Key Developments)
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            leftIndent=15,
            bulletIndent=0,
            fontName='Helvetica',
            textColor=self.TRUE_BLACK
        ))

        # Source citations
        self.styles.add(ParagraphStyle(
            name='SourceCitation',
            fontSize=9,
            leading=13,
            textColor=self.MED_GRAY,
            leftIndent=15,
            bulletIndent=0,
            fontName='Helvetica'
        ))

        # Outlook text (italicized)
        self.styles.add(ParagraphStyle(
            name='OutlookText',
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            fontName='Helvetica-Oblique',
            textColor=self.DARK_GRAY
        ))

    def generate_pdf(
        self,
        briefing: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate professional PDF from briefing JSON.

        Args:
            briefing: Briefing dict from BLUFSynthesizer
            output_path: Optional output path (default: data/pdfs/)

        Returns:
            Path to generated PDF
        """
        logger.info(f"Generating PDF for {briefing['region']} briefing...")

        # Setup output path
        if not output_path:
            output_dir = Path("data/pdfs")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y-%m-%d")
            region_slug = briefing['region'].lower().replace(' ', '_').replace('/', '_')
            output_path = output_dir / f"{region_slug}_{timestamp}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.5*inch,
            bottomMargin=0.6*inch
        )

        # Build content
        story = []
        story.extend(self._build_cover_page(briefing))
        story.append(PageBreak())
        story.extend(self._build_content(briefing))

        # Generate PDF with headers and footers
        doc.build(
            story,
            onFirstPage=self._draw_page_elements,
            onLaterPages=self._draw_page_elements
        )

        file_size = Path(output_path).stat().st_size / 1024
        logger.info(f"PDF generated: {output_path} ({file_size:.1f} KB)")
        return str(output_path)

    def _draw_page_elements(self, canvas, doc):
        """Draw header and footer on every page"""
        canvas.saveState()
        page_width, page_height = doc.pagesize

        # Top classification banner
        canvas.setFillColor(self.CLASSIFICATION_RED)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawCentredString(
            page_width / 2,
            page_height - 0.3 * inch,
            "UNCLASSIFIED // AI-GENERATED"
        )

        # Footer disclaimer
        canvas.setFillColor(self.MED_GRAY)
        canvas.setFont('Helvetica', 7)
        canvas.drawCentredString(
            page_width / 2,
            0.40 * inch,
            "UNCLASSIFIED // AI-GENERATED — Not official intelligence. Accuracy not guaranteed. Do not use for operational decision-making."
        )

        # Page number
        canvas.setFont('Helvetica', 8)
        canvas.drawCentredString(
            page_width / 2,
            0.25 * inch,
            f"SITREP Intelligence Platform — Page {doc.page}"
        )

        canvas.restoreState()

    def _build_cover_page(self, briefing: Dict) -> List:
        """Build professional cover page"""
        elements = []
        region = briefing.get('region', 'Unknown Region')
        generated_at = briefing.get('generated_at', datetime.utcnow().isoformat())

        # Format date
        try:
            gen_date = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            date_str = gen_date.strftime("%B %d, %Y")
        except:
            date_str = "Unknown Date"

        # Vertical spacing from top
        elements.append(Spacer(1, 1.8*inch))

        # Top classification marking
        classification = Paragraph(
            "UNCLASSIFIED // AI-GENERATED",
            self.styles['Classification']
        )
        elements.append(classification)
        elements.append(Spacer(1, 0.6*inch))

        # Main title: SITREP
        title = Paragraph("SITREP", self.styles['CoverTitle'])
        elements.append(title)

        # Subtitle: Intelligence Briefing
        subtitle = Paragraph(
            "Intelligence Briefing",
            self.styles['CoverSubtitle']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.4*inch))

        # Region
        region_para = Paragraph(region, self.styles['CoverRegion'])
        elements.append(region_para)

        # Date
        date_para = Paragraph(date_str, self.styles['CoverDate'])
        elements.append(date_para)
        elements.append(Spacer(1, 0.8*inch))

        # Professional disclaimer box
        disclaimer_content = """
        <para alignment="center">
        <font color="#8B0000" size="11"><b>⚠ AI-GENERATED CONTENT</b></font>
        </para>
        <para alignment="left" spaceBefore="8">
        This briefing is synthesized from open-source intelligence using
        artificial intelligence. Content is not official intelligence and should not
        be used for operational decision-making. Sources are cited but
        accuracy is not guaranteed. Use at your own discretion.
        </para>
        """

        disclaimer_para = Paragraph(disclaimer_content, self.styles['Normal'])
        disclaimer_table = Table(
            [[disclaimer_para]],
            colWidths=[5.5*inch]
        )
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.WARNING_BG),
            ('BOX', (0, 0), (-1, -1), 2, self.AMBER),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(disclaimer_table)

        return elements

    def _format_source(self, source: Union[str, Dict]) -> str:
        """
        Format source citation properly.

        Handles both old format (string) and new format (dict with source and title).
        Returns formatted citation string.
        """
        if isinstance(source, dict):
            # New format: {"source": "ISW", "title": "Article Title"}
            source_name = source.get('source', 'Unknown Source')
            title = source.get('title', 'Untitled')
            return f"<b>{source_name}</b>: {title}"
        else:
            # Old format: just a string title
            return str(source)

    def _build_content(self, briefing: Dict) -> List:
        """Build main briefing content with professional formatting"""
        elements = []

        # EXECUTIVE SUMMARY (BLUF)
        bluf_header = Paragraph("EXECUTIVE SUMMARY (BLUF)", self.styles['SectionHeader'])
        elements.append(bluf_header)

        # BLUF content in bordered box
        bluf_text = briefing.get('bluf', '')
        bluf_para = Paragraph(bluf_text, self.styles['BLUFContent'])

        bluf_table = Table([[bluf_para]], colWidths=[6.5*inch])
        bluf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.VERY_LIGHT_GRAY),
            ('BOX', (0, 0), (-1, -1), 3, self.AMBER),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(bluf_table)
        elements.append(Spacer(1, 0.25*inch))

        # KEY DEVELOPMENTS
        if briefing.get('key_developments'):
            key_dev_header = Paragraph("KEY DEVELOPMENTS", self.styles['SectionHeader'])
            elements.append(key_dev_header)

            for dev in briefing['key_developments']:
                bullet = Paragraph(f"• {dev}", self.styles['BulletPoint'])
                elements.append(bullet)
                elements.append(Spacer(1, 0.08*inch))

            elements.append(Spacer(1, 0.2*inch))

        # DETAILED ANALYSIS SECTIONS
        for section in briefing.get('sections', []):
            section_elements = []

            # Section title
            section_title = Paragraph(
                section['title'].upper(),
                self.styles['SectionHeader']
            )
            section_elements.append(section_title)

            # Section content
            content_para = Paragraph(
                section['content'],
                self.styles['BodyJustified']
            )
            section_elements.append(content_para)
            section_elements.append(Spacer(1, 0.15*inch))

            # Sources (formatted properly)
            if section.get('sources'):
                sources_header = Paragraph(
                    "<b>Sources:</b>",
                    self.styles['Normal']
                )
                sources_header.style.fontSize = 10
                section_elements.append(sources_header)

                for source in section['sources']:
                    formatted_source = self._format_source(source)
                    source_para = Paragraph(
                        f"• {formatted_source}",
                        self.styles['SourceCitation']
                    )
                    section_elements.append(source_para)

                section_elements.append(Spacer(1, 0.2*inch))

            # Keep section together on same page if possible
            elements.append(KeepTogether(section_elements))

        # OUTLOOK
        if briefing.get('outlook'):
            outlook_header = Paragraph("OUTLOOK", self.styles['SectionHeader'])
            elements.append(outlook_header)

            outlook_para = Paragraph(
                briefing['outlook'],
                self.styles['OutlookText']
            )
            elements.append(outlook_para)

        return elements


# Test function
def test_pdf_generator():
    """Test PDF generation with sample briefing"""
    briefing_path = Path(__file__).parent.parent / "data" / "briefings" / "middle_east_20260531_120618.json"

    if not briefing_path.exists():
        print(f"[ERROR] Test briefing not found: {briefing_path}")
        return

    with open(briefing_path, "r", encoding="utf-8") as f:
        briefing = json.load(f)

    # Generate PDF
    generator = PDFGenerator()
    pdf_path = generator.generate_pdf(briefing)

    print(f"[SUCCESS] PDF generated: {pdf_path}")
    print(f"File size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    test_pdf_generator()
