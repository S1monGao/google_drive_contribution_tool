from ast import literal_eval


def get_colour_from_text_style(style_string):
    """
    Converts the style attribute of an HTML element into a tuple of 3 rgb numbers
    :param style_string: The style attribute of the element
    :return: An rgb tuple, e.g. (0, 255, 62)
    """

    # Remove spaces and split by ";"
    style_string = style_string.replace(" ", "").split(";")

    # Search for colour section
    i = 0
    while "rgb" not in style_string[i]:
        i += 1
    colour_section = style_string[i]

    #Isolate tuple
    colour = colour_section.split(":")[1]
    colour_tuple = colour[3:]

    # Convert string that looks like a tuple to a tuple
    return literal_eval(colour_tuple)




if __name__ == "__main__":
    test1 = "font-size: 14.6667px; font-family: Arial; color: rgb(81, 45, 168); background-color: transparent; font-weight: 400; font-style: normal; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre;"
    print(get_colour_from_text_style(test1))
