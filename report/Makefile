RM=rm -rf

all: report.pdf

%.pdf: %.tex
	pdflatex $^
	pdflatex $^

clean:
	$(RM) *.pdf *.aux *.log *.out *.toc *.snm *.nav
