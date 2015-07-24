# markdown2tex

markdown2tex is a python script to convert markdown files into MLA-formatted LaTeX documents.

## MLA Document Formatting
markdown2tex uses a modified version template for an MLA LaTeX document associated with Ryan Aycock’s [mla-paper](http://www.ctan.org/tex-archive/macros/latex/contrib/mla-paper) LaTeX package - this must be installed for the script to run. This template stored in the ```/templates``` directory. When writing, use the following format to include metadata in your markdown document:
```markdown
# [TITLE]
## Author: [NAME]
## Teacher: [TEACHER]
## Class: [CLASS]

Paragraph 1

Paragraph 2

Paragraph 3

## Cite:
Citation 1
Citation 2
```
This will ensure that the generated LaTeX file has the correct information, and you will not need to manually edit the LaTeX file.

## Usage
markdown2tex in run as a traditional python file. Note that your terminal’s current working directory must be the ```markdown2tex``` folder. To use, simply run the following command:

```python
python mdtex.py input_file.md [-c] [--compile] [-v] [--verbose]
```
where input_file.md is the paper you wish to convert. The [-c]/[--compile] flag indicates that you want to not only format input_file.md as a LaTeX file, but also that you want to generate the PDF file with ```pdflatex``` (note that you must have pdflatex installed on your computer for this to work). The [-v]/[--verbose] flag indicates that you want to see the output of the conversion (and compilation) of the LaTeX file on the terminal.
