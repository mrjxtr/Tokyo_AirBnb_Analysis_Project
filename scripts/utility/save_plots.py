# def export_figs(fig, filename, export_dir):
#     import os

#     filepath = os.path.join(export_dir, filename)
#     fig.savefig(filepath)


def export_figs(fig, filename, export_dir, fig_number):
    import os

    formatted_number = f"fig{fig_number:03d}"
    prefixed_filename = f"fig{formatted_number}_{filename}"
    filepath = os.path.join(export_dir, prefixed_filename)
    fig.savefig(filepath)
