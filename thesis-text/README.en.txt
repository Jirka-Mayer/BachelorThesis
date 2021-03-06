A template for typesetting a bachelor thesis at MFF UK in LaTeX

Authors:

	Martin Mareš <mj@ucw.cz> -- the current maintainer
	Arnošt Komárek <komarek@karlin.mff.cuni.cz>
	Michal Kulich <kulich@karlin.mff.cuni.cz>

This package can be freely distributed, used, and modified.
If you have any bug report or comment, please tell us.
--------------------------------------------------------------------------------

There are two versions of the template -- Czech (directory "cs")
and English ("en").

Requirements on formatting of bachelor theses are given by Dean's directives
4/2019, 1/2015, and 7/2016, and by the Rector's directive 72/2017. Other
guidelines can be found in the example.pdf file. This LaTeX template follows
the directives; it also tries to emphasize important points in comments. Still,
we advise you to read the complete rules.

If you are not familiar with LaTeX yet, you can find numerous tutorials on
the Web. One example we like is http://en.wikibooks.org/wiki/LaTeX.

Basic typographical settings can be found in thesis.tex, which also refers
to all other files containing individual chapters. Please read the main file
carefully and fill in the thesis name, author, and other identifiers. You also
need to update the meta-data file thesis.xmpdata.

The Czech version contains several example chapters with hints on typesetting
of common expressions. There are not available in the English version yet,
sorry.

The electronic version of your thesis must be submitted to SIS. It must
conform to the PDF/A-1a or -2u standard. This template produces PDF/A-2u
using the pdfx LaTeX package (https://www.ctan.org/tex-archive/macros/latex/contrib/pdfx).
Please note that many installations of TeX have this package either obsolete
or broken. So we advise to download the current version of the package and
unpack it to tex/pdfx/.

Our FAQ on producing PDF/A is currently available in Czech only, but if you
encounter any problems, please ask Martin Mareš for advice.

If you are using Windows, beware that MikTeX contains old versions of some
(mostly mathematical) fonts, which leads to improper PDF/A output. We have
much better experience with the TeXlive distribution.

If you are using a UNIX system, you might want to use our example Makefile --
just run "make" to process all files by TeX.

You can also run TeX manually. In this case, you should use pdfTeX and also
BibTeX for generating bibliography. (The usual order is: pdflatex, bibtex,
and then pdflatex twice to get cross-references right. Alternatively, you
can use latexmk.)

The current development version of this template and other hints on writing
theses can be found at http://mj.ucw.cz/vyuka/bc/.
