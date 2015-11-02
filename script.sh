#!/bin/sh

#rodar duas vezes o Makefile
find -type f \( -name 'GNUmakefile' -o -name 'makefile' -o -name 'Makefile' \) \
-exec bash -c 'cd "$(dirname "{}")" && make' \;

find -type f \( -name 'GNUmakefile' -o -name 'makefile' -o -name 'Makefile' \) \
-exec bash -c 'cd "$(dirname "{}")" && make' \;

#mover os pdfs para raiz
find -type f \( -name '*pdf' \) \
-exec bash -c 'cd "$(dirname "{}")" && mv "$(basename "{}")" ../' \;

zip provas.zip *.pdf

#for i in $(ls *tex)
#do
#	#echo $i
#	pdflatex $i
#	#xelatex -shell-escape $i
#done
##rm provao.pdf
##%pdftk *.pdf cat output provas.pdf
#rm provas.zip
#zip provas.zip *.pdf
