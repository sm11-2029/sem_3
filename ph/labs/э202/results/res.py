from pathlib import Path
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_value(text):
    text = text.strip().replace(",", ".")
    text = text.replace("^", "**")
    return sp.sympify(text)


def read_data(filename):
    data = []

    with open(filename, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 4:
                continue
            if parts[0].lower().startswith("freq"):
                continue

            try:
                freq = parse_value(parts[0])
                umax = parse_value(parts[1])
                period = parse_value(parts[2])
                delay = parse_value(parts[3])
            except Exception:
                continue

            data.append((freq, umax, period, delay))

    return data


def make_rows(data):
    rows = []

    for freq, umax, period, delay in data:
        k = umax / 4
        phase = delay / period * 360
        rows.append((freq, k, phase))

    return rows


def latex_number(value, digits=3):
    return rf"\num[round-mode=places,round-precision={digits}]{{{float(value)}}}"


def latex_freq(value):
    return rf"\num[round-mode=places,round-precision=0]{{{float(value)}}}"


def make_table(rows):
    lines = [
        r"\begin{center}",
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"частота $f$, Гц & \hspace{1mm} $K_u(f)$ & \hspace{1mm} $\varphi(f)$, град. \\",
        r"\midrule",
    ]

    for freq, k, phase in rows:
        lines.append(
            f"{latex_freq(freq)} & {latex_number(k)} & {latex_number(phase)} \\\\"
        )

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{center}",
    ]

    return "\n".join(lines)


def make_plots(rows):
    freqs = [float(r[0]) for r in rows]
    ks = [float(r[1]) for r in rows]
    phases = [float(r[2]) for r in rows]

    specs = [
        (ks,     "$K_u$",             "k_lin.png",   "linear"),
        (phases, r"$\varphi$, град.", "phi_lin.png", "linear"),
        (ks,     "$K_u$",             "k_log.png",   "log"),
        (phases, r"$\varphi$, град.", "phi_log.png", "log"),
    ]

    for values, ylabel, filename, scale in specs:
        fig, ax = plt.subplots(figsize=(4.5, 2.8))

        if scale == "log":
            ax.semilogx(freqs, values, marker="o", markersize=3,
                        linewidth=1, color="black")
            ax.grid(True, which="both", alpha=0.3)
        else:
            ax.plot(freqs, values, marker="o", markersize=3,
                    linewidth=1, color="black")
            ax.grid(True, alpha=0.3)

        ax.set_xlabel("$f$, Гц")
        ax.set_ylabel(ylabel)
        fig.tight_layout()
        fig.savefig(filename, bbox_inches="tight", dpi=200)
        plt.close(fig)


def make_figure_cell(caption, filename):
    return (
        "\\begin{minipage}{0.5\\linewidth}\n"
        "\\centering\n"
        + caption + "\\\\[1mm]\n"
        "\\includegraphics[width=\\linewidth]{" + filename + "}\n"
        "\\end{minipage}"
    )


def make_figures_block(figures):
    # figures: [top_left, bottom_left, top_right, bottom_right]
    tl, bl, tr, br = figures

    row1 = make_figure_cell(*tl) + "\\hfill\n" + make_figure_cell(*tr)
    row2 = make_figure_cell(*bl) + "\\hfill\n" + make_figure_cell(*br)

    return (
        "\\begin{center}\n"
        + row1 + "\n\n\\vspace{0.4cm}\n\n"
        + row2 + "\n"
        "\\end{center}"
    )


def make_document(table, figures=None):
    figures_tex = ""

    if figures:
        figures_tex = make_figures_block(figures)

    return rf"""\documentclass[10pt,a5paper]{{article}}
\usepackage[margin=5mm]{{geometry}}
\usepackage[utf8]{{inputenc}}
\usepackage[T2A]{{fontenc}}
\usepackage[russian]{{babel}}
\usepackage{{booktabs}}
\usepackage{{amsmath}}
\usepackage{{graphicx}}
\pagestyle{{empty}}

\usepackage{{siunitx}}
\sisetup{{group-separator={{\,}}, group-minimum-digits=4}}

\begin{{document}}

\begin{{center}}
\Large Фильтр низких частот
\end{{center}}

\small
{table}

{figures_tex}

\end{{document}}
"""


def main():
    data = read_data("low_pass.txt")
    rows = make_rows(data)
    make_plots(rows)
    table = make_table(rows)

    figures = [
        (r"$K_u(f)$ в линейном масштабе",            "k_lin.png"),
        (r"$\varphi(f)$ в линейном масштабе",        "phi_lin.png"),
        (r"$K_u(f)$ в логарифмическом масштабе",     "k_log.png"),
        (r"$\varphi(f)$ в логарифмическом масштабе", "phi_log.png"),
    ]

    tex = make_document(table, figures)
    Path("res.tex").write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
