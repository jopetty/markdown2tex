def merge(input, output, control, spacer=False):
    index = -1
    offset = 0

    if (spacer != False): # Only add if declared
        for i in range(len(input)):
            input.insert(i*2, spacer) # Insert the spacer at even-numbered indicies in the input array

    for i in range(len(output)): # Find the location in the output file of the control sequence
        if output[i].startswith(control):
            index = i
            break # Stop searching the documnet

    if (index == -1): # Check to see if control sequence was found
        print u'WARNING: CONTROL SEQUENCE "' + control + u'" NOT FOUND'
    else:
        for i in range(index, index + len(input)): # Insert each line of the input into the output
            output.insert(index + offset + 1, input[offset])
            offset += 1 # Adjust offset to account for insertions
        output.pop(index) # Remove the control sequence
