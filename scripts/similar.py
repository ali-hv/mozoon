def similar(a, b):
    a = a.split()
    a_unique = []

    for j in a:
        if j not in a_unique:
            a_unique.append(j)

    b = b.split()
    b_unique = []

    for j in b:
        if j not in b_unique:
            b_unique.append(j)

    c = [j for j in a_unique if j in b_unique]
    
    total = len(a_unique)+len(b_unique)-len(c)
    ratio = len(c)/total

    return ratio