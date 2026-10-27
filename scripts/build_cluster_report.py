#!/usr/bin/env python3
"""Render verified keyword cluster JSON into an A4 PDF.

Usage: python scripts/build_cluster_report.py input.json output.pdf
Dependency: pip install reportlab
This script NEVER retrieves or fabricates SEO metrics.
"""
import json
import sys
from pathlib import Path
from html import escape

def generate(data, dest):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import mm

    for key in ("project", "topic", "created_at", "clusters"):
        if not data.get(key):
            raise ValueError("Missing required field: " + key)
    if not data.get("data_sources") and not data.get("is_demo"):
        raise ValueError("Real reports require data_sources. Never invent sources.")
    for cluster in data["clusters"]:
        for key in ("id", "primary_keyword", "intent", "content_type", "rationale"):
            if not cluster.get(key):
                raise ValueError(f"Cluster {cluster.get('id', '?')}: missing {key}")
        if not (cluster.get("evidence") or cluster.get("serp_snapshots")):
            raise ValueError("Cluster requires traceable evidence or SERP snapshot")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SEOBody", parent=styles["Normal"], fontSize=9, leading=13, spaceAfter=7))
    styles.add(ParagraphStyle(name="SEOTable", parent=styles["Normal"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="SEOHead", parent=styles["SEOTable"], textColor=colors.white))
    story = []
    def para(s, style="SEOBody"):
        return Paragraph(escape(str(s)), styles[style])
    story.append(para("SEO Research & Keyword Clustering", "Title"))
    story.append(para(f"{data['project']} | {data['topic']} | Stand: {data['created_at']}"))
    if data.get("is_demo"):
        story.append(para("DEMO: NO REAL RESEARCH DATA"))
    story.append(para("Status: DRAFT FOR HUMAN REVIEW. No writing without explicit approval."))
    story.append(para("Data sources", "Heading2"))
    for source in data.get("data_sources", []):
        story.append(para(f"{source.get('name', 'unknown')} | {source.get('retrieved_at', 'undated')} | {source.get('notes', '')}"))
    story.append(para("Cluster overview", "Heading2"))
    rows = [[para(x, "SEOHead") for x in ["ID", "Primary keyword", "Intent", "Content type"]]]
    for cl in data["clusters"]:
        rows.append([para(cl.get(k, ""), "SEOTable") for k in ("id", "primary_keyword", "intent", "content_type")])
    tab = Table(rows, colWidths=[26*mm, 57*mm, 40*mm, 47*mm], repeatRows=1)
    tab.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#20394F")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F0F4F7")]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(tab)
    for cl in data["clusters"]:
        story.append(para(f"Cluster {cl['id']}: {cl['primary_keyword']}", "Heading2"))
        for key, label in [("intent","Intent"),("content_type","Suggested page"),("rationale","Rationale"),
                           ("existing_url","Existing URL"),("target_url","Target URL"),("decision","User decision")]:
            story.append(para(f"{label}: {cl.get(key) or 'Not specified'}"))
        if cl.get("keywords"):
            story.append(para("Variants: " + ", ".join(cl["keywords"])))
        for e in cl.get("evidence", []):
            story.append(para("Evidence: " + str(e)))
        for sn in cl.get("serp_snapshots", []):
            story.append(para("SERP: " + json.dumps(sn, ensure_ascii=False)))
    story.append(para("Check the editable master sheet before approving any content production."))
    dest.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(dest), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm).build(story)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python scripts/build_cluster_report.py input.json output.pdf")
    generate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), Path(sys.argv[2]))
    print(sys.argv[2])
