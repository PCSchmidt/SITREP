# PDF Generator - Convert BLUF briefings to professional PDF documents
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Generates professional PDF briefings from BLUF JSON.

    Output format:
    - 15-20 pages typical
    - Military aesthetic (dark theme for screen, print-optimized)
    - BLUF format with sections
    - Source citations
    - Header/footer with metadata
    """

    def __init__(self):
        self.font_config = FontConfiguration()

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

        # Convert briefing to HTML
        html_content = self._briefing_to_html(briefing)

        # Generate PDF from HTML
        if not output_path:
            output_dir = Path("data/pdfs")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y-%m-%d")
            region_slug = briefing['region'].lower().replace(' ', '_').replace('/', '_')
            output_path = output_dir / f"{region_slug}_{timestamp}.pdf"

        # Convert HTML to PDF with WeasyPrint
        html = HTML(string=html_content)
        css = CSS(string=self._get_pdf_css())

        html.write_pdf(
            str(output_path),
            stylesheets=[css],
            font_config=self.font_config
        )

        logger.info(f"PDF generated: {output_path}")
        return str(output_path)

    def _briefing_to_html(self, briefing: Dict) -> str:
        """Convert briefing JSON to HTML"""
        region = briefing.get('region', 'Unknown Region')
        bluf = briefing.get('bluf', '')
        sections = briefing.get('sections', [])
        key_developments = briefing.get('key_developments', [])
        outlook = briefing.get('outlook', '')
        generated_at = briefing.get('generated_at', datetime.utcnow().isoformat())

        # Format date
        try:
            gen_date = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            date_str = gen_date.strftime("%B %d, %Y")
        except:
            date_str = "Unknown Date"

        # Build HTML
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='utf-8'>",
            f"<title>SITREP - {region} Intelligence Briefing</title>",
            "</head>",
            "<body>",

            # Cover page
            "<div class='cover-page'>",
            "<div class='classification'>UNCLASSIFIED // AI-GENERATED</div>",
            "<h1 class='title'>SITREP</h1>",
            "<h2 class='subtitle'>Intelligence Briefing</h2>",
            f"<div class='region'>{region}</div>",
            f"<div class='date'>{date_str}</div>",
            "<div class='disclaimer'>",
            "<p><strong>⚠️ AI-GENERATED CONTENT</strong></p>",
            "<p>This briefing is synthesized from open-source intelligence using artificial intelligence. ",
            "Content is not official intelligence and should not be used for operational decision-making. ",
            "Sources are cited but accuracy is not guaranteed. Use at your own discretion.</p>",
            "</div>",
            "</div>",

            # Page break before content
            "<div class='page-break'></div>",

            # Executive Summary (BLUF)
            "<div class='section'>",
            "<h2 class='section-header'>EXECUTIVE SUMMARY (BLUF)</h2>",
            f"<div class='bluf-content'>{bluf}</div>",
            "</div>",

            # Key Developments
            "<div class='section'>",
            "<h2 class='section-header'>KEY DEVELOPMENTS</h2>",
            "<ul class='key-developments'>",
        ]

        for dev in key_developments:
            html_parts.append(f"<li>{dev}</li>")

        html_parts.append("</ul>")
        html_parts.append("</div>")

        # Detailed Analysis Sections
        for section in sections:
            html_parts.append("<div class='section'>")
            html_parts.append(f"<h2 class='section-header'>{section['title'].upper()}</h2>")
            html_parts.append(f"<div class='section-content'>{section['content']}</div>")

            # Sources
            if section.get('sources'):
                html_parts.append("<div class='sources'>")
                html_parts.append("<h3 class='sources-header'>Sources:</h3>")
                html_parts.append("<ul class='source-list'>")
                for source in section['sources']:
                    html_parts.append(f"<li>{source}</li>")
                html_parts.append("</ul>")
                html_parts.append("</div>")

            html_parts.append("</div>")

        # Outlook
        if outlook:
            html_parts.append("<div class='section'>")
            html_parts.append("<h2 class='section-header'>OUTLOOK</h2>")
            html_parts.append(f"<div class='outlook-content'>{outlook}</div>")
            html_parts.append("</div>")

        # Footer
        html_parts.extend([
            "<div class='footer'>",
            "<p>Generated by SITREP Intelligence Platform</p>",
            f"<p>Report Date: {date_str}</p>",
            "<p>UNCLASSIFIED // AI-GENERATED</p>",
            "</div>",

            "</body>",
            "</html>"
        ])

        return "\n".join(html_parts)

    def _get_pdf_css(self) -> str:
        """CSS styling for PDF (military aesthetic, print-optimized)"""
        return """
        @page {
            size: Letter;
            margin: 0.75in;

            @top-center {
                content: "SITREP INTELLIGENCE BRIEFING";
                font-family: Arial, sans-serif;
                font-size: 10pt;
                color: #666;
            }

            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-family: Arial, sans-serif;
                font-size: 10pt;
                color: #666;
            }
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            background: #fff;
        }

        .cover-page {
            text-align: center;
            padding-top: 2in;
        }

        .classification {
            font-size: 12pt;
            font-weight: bold;
            color: #d00;
            letter-spacing: 2px;
            margin-bottom: 1in;
        }

        .title {
            font-size: 48pt;
            font-weight: bold;
            color: #000;
            letter-spacing: 4px;
            margin: 0;
        }

        .subtitle {
            font-size: 24pt;
            font-weight: normal;
            color: #333;
            margin-top: 0.2in;
        }

        .region {
            font-size: 18pt;
            font-weight: bold;
            color: #000;
            margin-top: 0.5in;
        }

        .date {
            font-size: 14pt;
            color: #666;
            margin-top: 0.2in;
        }

        .disclaimer {
            margin-top: 1in;
            padding: 0.25in;
            background: #fff3cd;
            border: 2px solid #FFA500;
            border-radius: 4px;
            text-align: left;
        }

        .disclaimer strong {
            color: #d00;
            font-size: 12pt;
        }

        .page-break {
            page-break-after: always;
        }

        .section {
            margin-bottom: 0.5in;
            page-break-inside: avoid;
        }

        .section-header {
            font-size: 16pt;
            font-weight: bold;
            color: #000;
            border-bottom: 2px solid #FFA500;
            padding-bottom: 0.1in;
            margin-top: 0.3in;
            margin-bottom: 0.2in;
            letter-spacing: 1px;
        }

        .bluf-content {
            font-size: 12pt;
            font-weight: bold;
            background: #f8f8f8;
            border-left: 4px solid #FFA500;
            padding: 0.2in;
            margin-bottom: 0.2in;
        }

        .section-content {
            text-align: justify;
            margin-bottom: 0.2in;
        }

        .key-developments {
            margin-left: 0.3in;
            line-height: 1.8;
        }

        .key-developments li {
            margin-bottom: 0.1in;
        }

        .sources {
            margin-top: 0.2in;
            padding-top: 0.1in;
            border-top: 1px solid #ccc;
        }

        .sources-header {
            font-size: 10pt;
            font-weight: bold;
            color: #666;
            margin-bottom: 0.05in;
        }

        .source-list {
            margin-left: 0.3in;
            font-size: 9pt;
            color: #666;
            line-height: 1.4;
        }

        .source-list li {
            margin-bottom: 0.05in;
        }

        .outlook-content {
            font-style: italic;
            background: #f0f0f0;
            padding: 0.15in;
            border-left: 3px solid #666;
        }

        .footer {
            margin-top: 0.5in;
            padding-top: 0.2in;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }

        .footer p {
            margin: 0.05in 0;
        }
        """


# Test function
def test_pdf_generator():
    """Test PDF generation with sample briefing"""
    # Load briefing
    with open("../data/briefings/europe_africa_2026-05-23.json", "r") as f:
        briefing = json.load(f)

    # Generate PDF
    generator = PDFGenerator()
    pdf_path = generator.generate_pdf(briefing)

    print(f"PDF generated: {pdf_path}")
    print(f"File size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    test_pdf_generator()
