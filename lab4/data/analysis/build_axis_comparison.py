"""Plot execution-axis RMSE from the archived metrics; no new measurement."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def build():
    here = Path(__file__).resolve().parent
    metrics = json.loads((here / 'metrics.json').read_text(encoding='utf-8'))
    values = [100 * x for x in metrics['execution_axis_rmse_m']]
    fig, ax = plt.subplots(figsize=(7, 3.1), layout='constrained')
    ax.bar(['X', 'Y', 'Z'], values, color=['#547a98', '#729f8b', '#b77857'], width=.55)
    for i, value in enumerate(values):
        ax.text(i, value + .12, f'{value:.2f} cm', ha='center', fontsize=11)
    ax.set(ylabel='Position RMSE (cm)', ylim=(0, 6.8),
           title='Execution interval: position error by axis')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=.2)
    ax.set_axisbelow(True)
    fig.savefig(here / 'axis_rmse_comparison.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    build()
