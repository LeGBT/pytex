import subprocess
import re
from random import shuffle


commands = [
    "lualatex",
    "-interaction=nonstopmode",
    "-halt-on-error",
    ]
builddir = "build/2016-2017"
outdir = "pdfs/2016-2017"
documentclass = "article"
documentclass_options = ["11pt", "a4paper"]
packages = []

geometry = "top=10mm, bottom=10mm, left=10mm, right=10mm"

preamble = [
    r"\setlength\parskip{\baselineskip}",
    r"\setlength\parindent{0pt}",
    r"\newunicodechar{ }{\ }",
    r"\setmainfont{Crimson Text}",
    r"\setmathfont{Asana Math}",
    ]

body = [""]


def pack(name, opt=""):
    if opt:
        packages.append(r"\usepackage[{0}]{{{1}}}".format(opt, name))
    else:
        packages.append(r"\usepackage{{{0}}}".format(name))

pack("amsmath")
pack("fontspec")
pack("unicode-math")
pack("newunicodechar")
pack("xcolor")
pack("tikz")
pack("pagecolor")
pack("enumerate")
pack("enumitem")
pack("siunitx", "locale = FR")
pack("macro")


def add(str_, *args):
    str_ = re.sub('{', '{{', str_)
    str_ = re.sub('}', '}}', str_)
    str_ = re.sub('’([^’]*)’', r'{\1}', str_)
    str_ = str_.format(*args)
    body.append(str_)


def section(str_):
    body.append("\n\section{{{0}}}\n".format(str_))


def subsection(str_):
    body.append("\n\subsection{{{0}}}\n".format(str_))


def toTEX(documentclass, documentclass_options,
          packages, body, name, correction=False):
    texpath = name+".tex"
    if documentclass_options:
        opts = ",".join(documentclass_options)
        dc = r"\documentclass[{0}]{{{1}}}".format(opts, documentclass)
    else:
        dc = r"\documentclass{{{0}}}".format(documentclass)
    if correction:
        conditionnals = ["\\correctiontrue"]
    else:
        conditionnals = ["\\correctionfalse"]
    tex = "\n".join(
            [dc] +
            [r"\usepackage["+geometry+r"]{geometry}"] +
            packages +
            preamble +
            conditionnals +
            [r"\begin{document}", body, r"\end{document}"])
    with open(name+".tex", "w") as f:
        f.write(tex)
    return texpath


def filter(output):
    lines = output.split("\n")
    result = []
    print_next = [
            ".*?:[0-9]+:",
            "!",
            "\w*TeX Warning",
            "\w*TeX warning",
            "^> [^<]",
            "^removed on input line",
                  ]
    info = ["Output written", "^This is \w*TeX"]
    warnings = ["^(Und|Ov)erfull", "^Package.*Warning"]
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


def compile(outname, correction=False, raw=False):
    b = "".join(body)
    if correction:
        print("\033[34;1mMode correction.\033[0m")
    buildname = "{0}/{1}".format(builddir, outname)
    correctionbuildname = "{0}/{1}".format(builddir, outname+"_correction")
    texPath = toTEX(documentclass, documentclass_options,
                    packages, b, buildname)
    corrtexPath = toTEX(documentclass, documentclass_options,
                        packages, b, correctionbuildname, correction=True)
    commands.append("--output-directory={0}/".format(builddir))
    args = commands + [texPath]
    correctionargs = commands + [corrtexPath]
    print("\033[34;1mCompilation : {0}\033[0m".format(" ".join(args)))
    try:
        output = subprocess.check_output(args).decode()
        subprocess.call(["mv", buildname+".pdf", outdir+"/"])
        if correction:
            subprocess.check_output(correctionargs).decode()
            subprocess.call(["mv", correctionbuildname+".pdf", outdir+"/"])
    except subprocess.CalledProcessError as e:
        output = (b"Erreur de compilation :\n"+e.output).decode()
    if not raw:
        filter(output)
    else:
        print(output)


# macros


def question(q, count, a, b, c, d, *args):
    res = [a, b, c, d]
    order = [0, 1, 2, 3]
    shuffle(order)
    bool1 = "1" if order[0] < count else "0"
    bool2 = "1" if order[1] < count else "0"
    bool3 = "1" if order[2] < count else "0"
    bool4 = "1" if order[3] < count else "0"
    add(r"""\qcm
    {"""+q+r"""}
    {"""+res[order[0]]+r"""}
    {"""+res[order[1]]+r"""}
    {"""+res[order[2]]+r"""}
    {"""+res[order[3]]+r"""}
    {"""+bool1+"} {"+bool2+"} {"+bool3+"} {"+bool4+r"""}
""", *args)
