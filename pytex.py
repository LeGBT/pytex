import subprocess

command = "pdflatex"
out = "build"
niveau = 4
entete = r"""
\documentclass{cours}
\def\leniveau{"""+str(niveau)+r"""}
\begin{document}
"""

body = " rien dedans "

end = "\end{document}"


def toTEX(src, name):
    texpath = name+".tex"
    with open(name+".tex", "w") as f:
        f.write(src)
    return texpath


def compile(outname):
    texPath = toTEX(entete+body+end, outname)
    args = [command, texPath, "--output-directory=", out]
    process = subprocess.Popen(args.split(), stdout=subprocess.PIPE)
    print(process.communicate()[0])
