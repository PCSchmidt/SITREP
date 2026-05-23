# PDF Generator using ReportLab (Windows-friendly alternative to WeasyPrint)
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generates professional PDF briefings from BLUF JSON using ReportLab.

    Output format:
    - 15-20 pages typical
    - Military aesthetic
    - BLUF format with sections
    - Source citations
    """

    # Colors
    AMBER = HexColor('#FFA500')
    GOLD = HexColor('#FFD700')
    DARK_GRAY = HexColor('#333333')
    LIGHT_GRAY = HexColor('#666666')
    WARNING_BG = HexColor('#fff3cd')

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        # Cover page title
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Title'],
            fontSize=48,
            textColor=black,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))

        # Section headers
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=black,
            spaceAfter=12,
            spaceBefore=18,
            fontName='Helvetica-Bold',
            borderColor=self.AMBER,
            borderWidth=2,
            borderPadding=6
        ))

        # BLUF content
        self.styles.add(ParagraphStyle(
            name='BLUF',
            parent=self.styles['BodyText'],
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY,
            leftIndent=10,
            borderColor=self.AMBER,
            borderWidth=3,
            borderPadding=12,
            backColor=HexColor('#f8f8f8'),
            fontName='Helvetica-Bold'
        ))

        # Normal body text
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY
        ))

        # Sources
        self.styles.add(ParagraphStyle(
            name='Source',
            parent=self.styles['BodyText'],
            fontSize=9,
            textColor=self.LIGHT_GRAY,
            leftIndent=20
        ))

    def generate_pdf(
        self,
        briefing: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate PDF from briefing JSON.

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
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build content
        story = []
        story.extend(self._build_cover_page(briefing))
        story.append(PageBreak())
        story.extend(self._build_content(briefing))

        # Generate PDF
        doc.build(story)

        file_size = Path(output_path).stat().st_size / 1024
        logger.info(f"PDF generated: {output_path} ({file_size:.1f} KB)")
        return str(output_path)

    def _build_cover_page(self, briefing: Dict) -> list:
        """Build cover page elements"""
        elements = []
        region = briefing.get('region', 'Unknown Region')
        generated_at = briefing.get('generated_at', datetime.utcnow().isoformat())

        # Format date
        try:
            gen_date = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            date_str = gen_date.strftime("%B %d, %Y")
        except:
            date_str = "Unknown Date"

        # Add spacing from top
        elements.append(Spacer(1, 1.5*inch))

        # Classification
        classification = Paragraph(
            "<font color='#d00000'><b>UNCLASSIFIED // AI-GENERATED</b></font>",
            self.styles['Normal']
        )
        classification.style.alignment = TA_CENTER
        classification.style.fontSize = 12
        elements.append(classification)
        elements.append(Spacer(1, 0.5*inch))

        # Title
        title = Paragraph("SITREP", self.styles['CoverTitle'])
        elements.append(title)

        # Subtitle
        subtitle = Paragraph(
            "<font size=24>Intelligence Briefing</font>",
            self.styles['Normal']
        )
        subtitle.style.alignment = TA_CENTER
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))

        # Region
        region_text = Paragraph(
            f"<font size=18><b>{region}</b></font>",
            self.styles['Normal']
        )
        region_text.style.alignment = TA_CENTER
        elements.append(region_text)
        elements.append(Spacer(1, 0.1*inch))

        # Date
        date_text = Paragraph(
            f"<font size=14 color='#666666'>{date_str}</font>",
            self.styles['Normal']
        )
        date_text.style.alignment = TA_CENTER
        elements.append(date_text)
        elements.append(Spacer(1, 0.75*inch))

        # Disclaimer
        disclaimer_text = """
        <font color='#d00000'><b>⚠ AI-GENERATED CONTENT</b></font><br/>
        <br/>
        This briefing is synthesized from open-source intelligence using artificial intelligence.
        Content is not official intelligence and should not be used for operational decision-making.
        Sources are cited but accuracy is not guaranteed. Use at your own discretion.
        """

        disclaimer_table = Table(
            [[Paragraph(disclaimer_text, self.styles['Normal'])]],
            colWidths=[5.5*inch]
        )
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.WARNING_BG),
            ('BOX', (0, 0), (-1, -1), 2, self.AMBER),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(disclaimer_table)

        return elements

    def _build_content(self, briefing: Dict) -> list:
        """Build main content elements"""
        elements = []

        # Executive Summary (BLUF)
        elements.append(Paragraph("EXECUTIVE SUMMARY (BLUF)", self.styles['SectionHeader']))
        elements.append(Paragraph(briefing.get('bluf', ''), self.styles['BLUF']))
        elements.append(Spacer(1, 0.3*inch))

        # Key Developments
        if briefing.get('key_developments'):
            elements.append(Paragraph("KEY DEVELOPMENTS", self.styles['SectionHeader']))
            for dev in briefing['key_developments']:
                elements.append(Paragraph(f"• {dev}", self.styles['BodyJustified']))
                elements.append(Spacer(1, 0.1*inch))
            elements.append(Spacer(1, 0.3*inch))

        # Detailed Analysis Sections
        for section in briefing.get('sections', []):
            # Section title
            elements.append(Paragraph(section['title'].upper(), self.styles['SectionHeader']))

            # Section content
            elements.append(Paragraph(section['content'], self.styles['BodyJustified']))
            elements.append(Spacer(1, 0.2*inch))

            # Sources
            if section.get('sources'):
                elements.append(Paragraph("<b>Sources:</b>", self.styles['Normal']))
                for source in section['sources']:
                    elements.append(Paragraph(f"• {source}", self.styles['Source']))
                elements.append(Spacer(1, 0.2*inch))

        # Outlook
        if briefing.get('outlook'):
            elements.append(Paragraph("OUTLOOK", self.styles['SectionHeader']))
            outlook_text = f"<i>{briefing['outlook']}</i>"
            elements.append(Paragraph(outlook_text, self.styles['BodyJustified']))

        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer_lines = [
            "<font size=9 color='#666666'>Generated by SITREP Intelligence Platform</font>",
            "<font size=9 color='#666666'>UNCLASSIFIED // AI-GENERATED</font>"
        ]
        for line in footer_lines:
            p = Paragraph(line, self.styles['Normal'])
            p.style.alignment = TA_CENTER
            elements.append(p)

        return elements


# Test function
def test_pdf_generator():
    """Test PDF generation with sample briefing"""
    # Load briefing
    briefing_path = Path(__file__).parent.parent.parent / "data" / "briefings" / "europe_africa_2026-05-23.json"
    with open(briefing_path, "r", encoding="utf-8") as f:
        briefing = json.load(f)

    # Generate PDF
    generator = PDFGenerator()
    pdf_path = generator.generate_pdf(briefing)

    print(f"[SUCCESS] PDF generated: {pdf_path}")
    print(f"File size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    test_pdf_generator()
