from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_executive_pdf(summary):
    """Generates a PDF buffer from the executive summary dictionary."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(summary.get("title", "Executive Summary"), styles['Title']))
    story.append(Spacer(1, 12))

    # Define the sections to include in order
    sections = [
        ("🎯 Objective", "objective"),
        ("📊 Key Outcomes", "key_outcomes"),
        ("🧠 Methodology", "methodology"),
        ("📈 Key Insights", "key_insights"),
        ("💼 Business Impact", "business_impact"),
        ("🏛️ Policy Impact", "policy_impact"),
        ("🚀 Recommendations", "recommendations"),
        ("📌 Conclusion", "conclusion")
    ]

    for label, key in sections:
        story.append(Paragraph(label, styles['Heading2']))
        content = summary.get(key, "")
        if isinstance(content, list):
            for item in content:
                story.append(Paragraph(item, styles['Normal'], bulletText="•"))
        else:
            story.append(Paragraph(str(content), styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer