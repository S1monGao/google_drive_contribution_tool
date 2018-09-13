dec_widths = [] # An array of decorations (strikethroughs that denote a deletion) for a paragraph in the form (width, colour), e.g. (10.00, (100,0,255))
contents = [] # An array of sections from a paragraph in the form (width, colour, content), e.g. (100.00 (100,0,255), "Test content")

deletions = [] # Stores all contents that correpsond to deletions
additions = [] # Same for additions

for content in contents:
    deletion_found = False
    for dec_width in dec_widths:
        if abs(dec_widths[0] - content[0]) < 1 and dec_width[1] == content[1]: # We can match a decoration with the content if they have similar length and same colour
            deletions.append(content)
            deletion_found = True
        if deletion_found:
            dec_widths.remove(dec_width)
            break
    if not deletion_found:
        additions.append(content)

