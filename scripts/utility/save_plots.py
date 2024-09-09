def export_figs(export_dir, fig, fig_number, filename):
    import os

    formatted_number = f"fig_{fig_number:03d}"
    prefixed_filename = f"{formatted_number}_{filename}"
    filepath = os.path.join(export_dir, prefixed_filename)
    fig.savefig(filepath)
