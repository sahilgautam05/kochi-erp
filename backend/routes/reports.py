import io
from datetime import datetime
from fastapi import APIRouter, Query, Response
from database import get_db_connection

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

router = APIRouter(prefix="/api/report", tags=["PDF Reports"])

def create_header(title: str, subtitle: str):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12
    )
    elements = [
        Paragraph("<b>KOCHI METRO RAIL LIMITED (KMRL)</b>", title_style),
        Paragraph(f"{title} &bull; Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", subtitle_style),
        Paragraph(f"<i>{subtitle}</i>", styles['Normal']),
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=15)
    ]
    return elements

@router.get("/status-pdf")
def generate_status_pdf():
    """
    Generates PDF report for Train Eligibility & Operating Status.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, status, alerts, mileage, branding, stabling FROM train_rules").fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = create_header("Train Status & Eligibility Report", "Official Fleet Compliance & Maintenance Clearance Document")

    styles = getSampleStyleSheet()

    # Table Header & Rows
    table_data = [["Train ID", "Train Name", "Status", "Mileage (km)", "Bay / Track", "Alerts"]]
    eligible_count = 0
    blocked_count = 0

    for r in rows:
        status_str = r["status"]
        if status_str == "Eligible":
            eligible_count += 1
        else:
            blocked_count += 1

        table_data.append([
            r["id"],
            r["name"],
            r["status"],
            f"{r['mileage']:,}" if r['mileage'] else "N/A",
            r["stabling"] or "-",
            r["alerts"] or "None"
        ])

    # Summary box
    summary_data = [
        ["Total Trains Evaluated", "Eligible for Service", "Blocked / Under Maintenance", "Operational Readiness"],
        [str(len(rows)), str(eligible_count), str(blocked_count), f"{(eligible_count/max(1, len(rows)))*100:.1f}%"]
    ]
    summary_table = Table(summary_data, colWidths=[130, 130, 140, 140])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#1e293b")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 15))

    # Main data table
    t = Table(table_data, colWidths=[65, 120, 75, 85, 85, 110])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (3, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)

    doc.build(elements)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=kmrl-status-report.pdf"}
    )

@router.get("/whatif-pdf")
def generate_whatif_pdf(
    k: int = Query(10),
    branding_weight: float = Query(0.5),
    stabling_weight: float = Query(0.3)
):
    """
    Generates PDF report for What-If Optimization Analysis.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, status, alerts, mileage, branding, stabling FROM train_rules").fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = create_header("What-If Scenario Optimization Report", f"Simulation Parameters: Top K={k} trains, Branding Weight={branding_weight}, Stabling Weight={stabling_weight}")

    table_data = [["Train ID", "Train Name", "Baseline Mileage (km)", "Branding Partner", "Stabling Position", "Optimized Score"]]

    for r in rows[:max(1, k)]:
        base_mileage = r["mileage"] or 50000
        norm_score = max(10.0, 100.0 - (base_mileage / 1500.0))
        brand_val = 20.0 if r["branding"] and r["branding"] != "None" else 5.0
        stabling_val = 15.0 if "Bay" in (r["stabling"] or "") else 8.0
        calculated_score = round((norm_score * 0.5) + (brand_val * float(branding_weight) * 2.0) + (stabling_val * float(stabling_weight) * 2.0), 2)

        table_data.append([
            r["id"],
            r["name"],
            f"{base_mileage:,}",
            r["branding"] or "None",
            r["stabling"] or "-",
            f"{calculated_score:.2f}"
        ])

    t = Table(table_data, colWidths=[65, 120, 110, 100, 85, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('ALIGN', (5, 1), (5, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f9ff")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)

    doc.build(elements)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=kmrl-whatif-report.pdf"}
    )

@router.get("/alerts-pdf")
def generate_alerts_pdf():
    """
    Generates PDF report for System Alerts & Faults Distribution.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, status, alerts, mileage, stabling FROM train_rules").fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = create_header("Fleet Alerts & Maintenance Distribution Report", "Active System Warnings, Equipment Flags, and Service Impediments")

    table_data = [["Train ID", "Train Name", "Operating Status", "Active Alert Description", "Location"]]
    
    alert_counts = {}
    for r in rows:
        if r["alerts"] and r["alerts"] != "-":
            for alert in r["alerts"].split(","):
                a_clean = alert.trim() if hasattr(alert, 'trim') else alert.strip()
                alert_counts[a_clean] = alert_counts.get(a_clean, 0) + 1
            table_data.append([
                r["id"],
                r["name"],
                r["status"],
                r["alerts"],
                r["stabling"] or "Depot"
            ])
        else:
            table_data.append([
                r["id"],
                r["name"],
                r["status"],
                "Normal - No Alerts",
                r["stabling"] or "In Service"
            ])

    t = Table(table_data, colWidths=[65, 125, 85, 175, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d97706")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#fffbeb")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)

    doc.build(elements)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=kmrl-alerts-report.pdf"}
    )
