"""Build Chinese and English versions of the two individual deliverables."""
from render_template_reports import build_template_report

if __name__ == '__main__':
    for number in (1, 2):
        build_template_report(f'Deliverable_{number}_EN.md',
                              f'deliverable_{number}.pdf', english=True)
        build_template_report(f'Deliverable_{number}_CN.md',
                              f'deliverable_{number}_CN.pdf', english=False)
