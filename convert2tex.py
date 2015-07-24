import subprocess
import os
from merge import *

########################################## VARIABLES

# Declare unicode array of replacement characters
# Note that doubled sequences (like **:BOLD) must appear before single sequences (like *:ITALIC) in the array; otherwise the replace function will incorrectly replace the single sequences inside of the doubled sequences, resulting in something like the following:
#  **DATA**     >>>     \textit{\textit{DATA}}
# instead of
# **DATA**      >>>     \textbf{DATA}
rep_array = [
    # Characters used by iA Writer
    [u'\u2018', "`"], # LEFT SINGLE QUOTATION MARK > APOSTROPHE
    [u'\u2019', "'"], # RIGHT SINGLE QUOTATION MARK > APOSTROPHE
    [u'\u201C', "``"], # LEFT DOUBLE QUOTATION MARK > GRAVE ACCENT x2
    [u'\u201D', '"'], # RIGHT DOUBLE QUOTATION MARK > QUOTATION MARK
    [u'\u2026', '...'], # HORIZONTAL ELLIPSIS > FULL STOP x3

    # MLA formatting sequences
    [u'\u002e\u0020', u'\u002e\u0020\u005c\u0020'], # SINGLE SPACING -> DOUBLE SPACING
    [u'\u0020\u0022', u'\u0020``'], # LEFT DOUBLE QUOTATION MARK > GRAVE ACCENT x2

    # Markdown formatting sequences
    [u'\u0020**', u'\u0020\u005ctextbf{'], # MARKDOWN BOLD TEXT START ( **)
    [u'**\u0020', u'}\u0020'], # MARKDOWN BOLD TEXT END (** )
    [u'\u0020*', u'\u0020\u005ctextit{'], # MARKDOWN ITALIC TEXT START ( *)
    [u'*\u0020', u'}\u0020'], # MARKDOWN ITALIC TEXT END (* )
]

# Declare structure variables


########################################## METHODS

def replace_chars(text):
    for i in range(len(text)):
        for j in range(len(rep_array)):
            text[i] = text[i].replace(rep_array[j][0], rep_array[j][1])

def structure_text(text, template):
    title = ''
    author_name = []
    teacher_name = ''
    class_name = ''
    bibliography = []

    pop_list = []
    offset = 0

    # Set the structure variables
    for i in range(len(text)):
        if text[i].startswith(u'\u0023\u0020'): # Title of the document (# [TITLE])
            title = text[i][2:].strip('\n')
            pop_list.append(i)
        elif text[i].startswith(u'\u0023\u0023\u0020Author:\u0020'): # Author of the document (## Author: [AUTHOR])
            author_name = text[i][11:].strip('\n').split(' ')
            pop_list.append(i)
        elif text[i].startswith(u'\u0023\u0023\u0020Teacher:\u0020'): # Teacher of the document (## Teacher: [TEACHER])
            teacher_name = text[i][12:].strip('\n')
            pop_list.append(i)
        elif text[i].startswith(u'\u0023\u0023\u0020Class:\u0020'): # Class name for the document (## Class: [CLASS])
            class_name = text[i][10:].strip('\n')
            pop_list.append(i)
        elif text[i].startswith(u'\u0023\u0023\u0020Cite:'): # Citations for the document (## Cite: \n [ENTRY] \n [ENTRY])
            pop_list.append(i)
            for j in range(i+1, len(text)): # Add ALL lines after the (## Cite:) to the bibliography
                text[j] += u'\n'
                bibliography.append(text[j])
                pop_list.append(j)

    # Format the bibliography
    replace_chars(bibliography)

    # Merge the structure variables with the template
    for i in range(len(template)):
        template[i] = template[i].replace('TITLE', title)
        template[i] = template[i].replace('FIRSTNAME', author_name[0])
        template[i] = template[i].replace('LASTNAME', author_name[1])
        template[i] = template[i].replace('CLASS', class_name)
        template[i] = template[i].replace('TEACHER', teacher_name)

    merge(bibliography, template, u'\u0025\u0020BEGIN\u0020WORKS\u0020CITED\u0020HERE', u'\u005cbibent\n')

    for i in pop_list: # Remove the metadata from essay once structure variables have been assigned
        text.pop(i - offset) # Remove the item from the list
        offset += 1 # Increment the offset to account for the previous item removal

def minify(text):
    pop_list = []
    offset = 0

    for i in range(len(text)):
        if ((text[i] == '') or (text[i] == '\n')): # Check to see if the line is empty (error) or only a carriage return
            pop_list.append(i)

    for i in pop_list: # Remove any blank or carriage return lines
        text.pop(i - offset)
        offset += 1

def gen_pdf(file_path, file_name, flag_v): # Use pdflatex to generate a PDF output
    bash_cmd = 'pdflatex ' + file_name # Set the bash command to pdflatex [FILENAME]

    if (flag_v):
        print '>> ' + bash_cmd # Print bash_cmd
        gen = subprocess.Popen(bash_cmd.split(), cwd=file_path) # Write all output to terminal
    else:
        with open(os.devnull, 'w') as FNULL: # Open DEVNULL for writing
            gen = subprocess.Popen(bash_cmd.split(), cwd=file_path, stdout=FNULL) # Write all output to DEVNULL
        FNULL.close() # Close DEVNULL

    output = gen.communicate()[0] # Terminate pdflatex and open terminal for input
