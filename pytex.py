import subprocess
import re
import os


commands = [
    "lualatex",
    "-interaction=nonstopmode",
    "-halt-on-error"
    ]
out = "build"
documentclass = "article"
documentclass_options = ["12pt", "a4paper"]
packages = []

preamble = [
    r"\geometry{margin=20mm}",
    r"\setlength\parskip{\baselineskip}",
    r"\setlength\parindent{0pt}",
    r"\newunicodechar{ }{\ }",
    r"\setmainfont{Crimson Text}",
    r"\setmathfont{Asana Math}",
    ]

body = "Ce document est vide."


def pack(name, opt=""):
    if opt:
        packages.append(r"\usepackage[{0}]{{{1}}}".format(opt, name))
    else:
        packages.append(r"\usepackage{{{0}}}".format(name))

pack("geometry")
pack("amsmath", "fleqn")
pack("fontspec")
pack("unicode-math")
pack("newunicodechar")


def toTEX(documentclass, documentclass_options, packages, src, name):
    texpath = name+".tex"
    if documentclass_options:
        opts = ",".join(documentclass_options)
        dc = r"\documentclass[{0}]{{{1}}}".format(opts, documentclass)
    else:
        dc = r"\documentclass{{{0}}}".format(documentclass)
    tex = "\n".join(
            [dc] +
            packages +
            preamble +
            [r"\begin{document}", src, r"\end{document}"])
    with open(name+".tex", "w") as f:
        f.write(tex)
    return texpath


def filter(output):
    lines = output.split("\n")
    result = []
    print_next = [
            ".*?:[0-9]+:",
            "!",
            "\w*TeX warning",
            "^> [^<]",
            "^removed on input line",
                  ]
    info = ["Output written", "^This is \w*TeX"]
    warnings = ["^(Und|Ov)erfull", "^(LaTeX|Package).*Warning"]
    errors = [
        "^ No pages of output",
        "^(LaTeX|Package).*Error",
        "Citation.*undefined",
        " Error",
        "^Missing character:",
        "^\*\*\*",
        "^l\.[0-9]+",
        "^all text was ignored after line",
        "Fatal error",
        "for symbol.*on input line",
            ]

    def comp(l): return [re.compile(pattern) for pattern in l]

    def match(l, line): return [1 for pattern in l if pattern.match(line)]
    print_next = comp(print_next)
    info = comp(info)
    warnings = comp(warnings)
    errors = comp(errors)
    for i, line in enumerate(lines):
        # print next
        if match(print_next, line):
            result.append((i, 2))
            result.append((i+1, 2))
        else:
            # print valid line
            if match(info, line):
                result.append((i, 0))
            if match(warnings, line):
                result.append((i, 1))
            if match(errors, line):
                result.append((i, 2))
    colors = ['\033[32;1m', '\033[33;1m', '\033[31;1m']
    for r in result:
        print(colors[r[1]]+lines[r[0]]+'\033[0m')


def compile(outname):
    texPath = toTEX(documentclass, documentclass_options,
                    packages, body, outname)
    args = commands + [texPath]
    print("\033[34;1mCompiling: {0}\033[0m".format(" ".join(args)))
    try:
        my_env = os.environ
        my_env["max_print_line"] = "1000"
        output = subprocess.check_output(args, env=my_env).decode()
    except subprocess.CalledProcessError as e:
        output = (b"Failed compilation:\n"+e.output).decode()
    filter(output)
