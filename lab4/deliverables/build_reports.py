"""Rebuild the English theory deliverables and both experiment reports."""
from render_template_reports import build_template_report

if __name__ == '__main__':
    build_template_report('Deliverable_1_EN.md', 'deliverable_1.pdf', english=True)
    build_template_report('Deliverable_2_EN.md', 'deliverable_2.pdf', english=True)
    build_template_report()
    build_template_report('Lab4_Report_EN.md', 'Lab4_Report_EN_Boyu_Huang.pdf', english=True)
