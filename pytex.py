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
    rep1 = order.index(0)
    rep2 = order.index(1)
    rep3 = order.index(2)
    rep4 = order.index(3)
    x1 = "\hcl" if (rep1//2) else "0"
    y1 = "2" if (rep1 % 2) else "0"
    x2 = "\hcl" if (rep2//2) else "0"
    y2 = "2" if (rep2 % 2) else "0"
    x3 = "\hcl" if (rep3//2) else "0"
    y3 = "2" if (rep3 % 2) else "0"
    x4 = "\hcl" if (rep4//2) else "0"
    y4 = "2" if (rep4 % 2) else "0"
    add("\\def\\pytexq{"+q+"}%\n" +
        "\\def\\pytexa{"+res[order[0]]+"}%\n" +
        "\\def\\pytexb{"+res[order[1]]+"}%\n" +
        "\\def\\pytexc{"+res[order[2]]+"}%\n" +
        "\\def\\pytexd{"+res[order[3]]+"}%\n", *args)
    add("\\boolatrue" +
        "\\def\\pytexxa{"+x1+"}%\n" +
        "\\def\\pytexya{"+y1+"}%\n")
    if count > 1:
        add("\\boolbtrue" +
            "\\def\\pytexxb{"+x2+"}%\n" +
            "\\def\\pytexyb{"+y2+"}%\n")
    else:
        add("\\boolbfalse")

    if count > 2:
        add("\\boolctrue" +
            "\\def\\pytexxc{"+x3+"}%\n" +
            "\\def\\pytexyc{"+y3+"}%\n")
    else:
        add("\\boolcfalse")

    if count > 3:
        add("\\booldtrue" +
            "\\def\\pytexxd{"+x4+"}%\n" +
            "\\def\\pytexyd{"+y4+"}%\n")
    else:
        add("\\booldfalse")

    add("\\qcm")
