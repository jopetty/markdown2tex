import os
import codecs
import argparse
import ntpath
from convert2tex import *
from merge import *

# Declare template file
mla_template = 'templates/mla.tex'

# Define the conversion method
def convert(essay, template):
    minify(template)
    structure_text(essay, template)
    replace_chars(essay)

def main(input_file, is_compile, is_verbose):

    fp, fn = ntpath.split(input_file)

    with open(mla_template, 'r') as template_file: # Open the final template file for reading
        template = template_file.readlines() # Read lines of the template file

        with codecs.open(input_file, 'r', encoding='utf-8') as essay_file: # Open the *.md file for reading
            essay = essay_file.readlines() # Read lines in *.md file
            if (is_verbose):
                print 'Reading data from ' + input_file

            convert(essay, template) # Convert markdown to tex
            if (is_verbose):
                print 'Converting ' + fn + ' to a LaTeX file'

            merge(essay, template, u'\u0025\u0020BEGIN\u0020ESSAY\u0020HERE') # Combine the essay and the template
            if (is_verbose):
                print 'Merging data from ' + fn + ' with template ' + ntpath.split(mla_template)[1]

            tex_path = fp + '/' + os.path.splitext(fn)[0] + '.tex' # Create the file path of the .tex file

            with codecs.open(tex_path, 'w+', encoding='utf-8') as mla_tex: # Open (create) the *.tex file for editing
                if (is_verbose):
                    print 'Writing data to ' + ntpath.split(tex_path)[1]
                for line in template:
                    mla_tex.write(line)
            mla_tex.close()
        essay_file.close()
    template_file.close()

    if (is_compile == True):
        if (is_verbose):
            print 'Generating ' + os.path.splitext(ntpath.split(tex_path)[1])[0] + '.pdf from ' + ntpath.split(tex_path)[1]
            gen_pdf(ntpath.split(tex_path)[0], ntpath.split(tex_path)[1], True)
        else:
            gen_pdf(ntpath.split(tex_path)[0], ntpath.split(tex_path)[1], False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a script to convert markdown files into MLA-ready LaTeX documents')
    parser.add_argument('input_file', help='FULL PATH of markdown file you want to convert')
    parser.add_argument('-c','--compile', help='Compile the *.tex file into a LaTeX PDF', action='store_true')
    parser.add_argument('-v', '--verbose', help='Increase the verbosity of output', action='store_true')
    args = parser.parse_args()
    main(args.input_file, args.compile, args.verbose)
