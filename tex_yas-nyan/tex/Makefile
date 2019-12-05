LATEX = platex --kanji=utf8:
BIBTEX = bibtex
OUTUNI = out2uni 
# しおりの文字化け回避のライブラリ。古いので.tex上にatbegshを利用する記述を追加して対応する。20171201 @yas-nyan
DVI2PS = dvips
DVIPDF = dvipdfmx
DVI_VIEW = xdvi
PS_VIEW = gv
PS2PDF = ps2pdf
PUBLICHTML = ./pdf/
NAME = b_thesis
TEXHTML = latex2html

# 現状,allだけではbib関連がバグる．make dvi bib pdfを手動でやる．
all:pdf

ps_view: ps
	$(PS_VIEW) $(NAME).ps

pdf: dvi bib dvi bib
	#$(LATEX) $(NAME).tex
	$(DVIPDF) $(NAME)
	#cp $(NAME).pdf $(PUBLICHTML)/

bib: 
	$(BIBTEX) $(NAME)

#pptsubmit:
#	cp $(PUBLICHTML)/paper/$(NAME).ppt /mnt/auspex/htdoc0/htdocs/rg/2002f/bachelor-presen/materials/irino.ppt
#	cp $(PUBLICHTML)/paper/$(NAME)/irino.htm /mnt/auspex/htdoc0/htdocs/rg/2002f/bachelor-presen/materials/
#	cp -r $(PUBLICHTML)/paper/$(NAME)/irino.files /mnt/auspex/htdoc0/htdocs/rg/2002f/bachelor-presen/materials/

ps2pdf: ps
	$(PS2PDF) $(NAME).ps

ps: dvi
	$(DVI2PS) $(NAME).dvi

dvi_view: dvi
	$(DVI_VIEW) $(NAME).dvi &

dvi : $(NAME).tex
	$(LATEX) $(NAME).tex
	#$(BIBTEX) $(NAME)

html : 
	$(TEXHTML) $(NAME).tex
	mv $(NAME) $(PUBLICHTML)/paper/

clean:
	rm -f $(NAME).ps *.aux *.dvi *.aux *.log *.bbl *.blg *.out *.tmp *.lot *.toc *.lof *.fls *.fdb_latexmk core  *~
