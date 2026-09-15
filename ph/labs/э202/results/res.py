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

\usepackage{{siunitx}}
\sisetup{{group-separator={{\,}}, group-minimum-digits=4}}

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
