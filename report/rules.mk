CLEAN := $(CLEAN) report/*.pdf report/*.aux report/*.log \
	report/*.out report/*.toc report/*.snm report/*.nav

report: report/report.pdf

report/%.pdf: report/%.tex
	cd report; \
	pdflatex report.tex; \
	pdflatex report.tex
