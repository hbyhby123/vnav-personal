"""Compatibility entry point for the current template-based reports."""
from render_template_reports import build_template_report


def build_readable_report(source_name='实验报告.md', target_name='Lab4_实验报告_黄博宇.pdf', english=False):
    return build_template_report(source_name, target_name, english)


if __name__ == '__main__':
    build_readable_report()
