from pathlib import Path
import sympy as sp


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


def latex_number(value):
    value = float(value)

    if abs(value - round(value)) < 1e-9:
        expr = sp.Integer(int(round(value)))
    else:
        expr = sp.Float(str(round(value, 3)))

    return sp.latex(expr)


def make_table(rows):
    lines = [
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"Frequency (Hz) & \(K\) & Phase (deg) \\",
        r"\midrule",
    ]

    for freq, k, phase in rows:
        lines.append(
            f"{latex_number(freq)} & {latex_number(k)} & {latex_number(phase)} \\\\"
        )

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
    ]

    return "\n".join(lines)


def make_document(table, plot_file=None):
    plot = ""

    if plot_file:
        plot = (
            "\\vspace{0.5cm}\n"
            "\\includegraphics[width=\\linewidth]{" + plot_file + "}\n"
        )

    return rf"""\documentclass[10pt,a5paper]{{article}}
\usepackage[margin=1.2cm]{{geometry}}
\usepackage[utf8]{{inputenc}}
\usepackage[T2A]{{fontenc}}
\usepackage[russian]{{babel}}
\usepackage{{booktabs}}
\usepackage{{amsmath}}
\usepackage{{graphicx}}
\pagestyle{{empty}}

\begin{{document}}

\small
{table}

{plot}

\end{{document}}
"""


def main():
    data = read_data("low_pass.txt")
    rows = make_rows(data)
    table = make_table(rows)
    tex = make_document(table)

    Path("res.tex").write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
