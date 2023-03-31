#!/bin/bash

mkdir -p figures_pdf

for filename in `ls figures_svg/*.svg` ; do
	inkscape -D -z --file=${filename} --export-pdf=${filename//svg/pdf}
done
