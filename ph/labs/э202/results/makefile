all: clean_aux

res.tex: res.py low_pass.txt
	python3 res.py

res.pdf: res.tex
	pdflatex res.tex

clean_aux: res.pdf
	rm *.png res.tex res.aux res.log res.out res.toc

clean:
	rm res.tex res.pdf res.aux res.log
