        # dependent on c ratio move up to the original
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")