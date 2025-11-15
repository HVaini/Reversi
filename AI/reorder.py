def reorder_moves(board, player, moves):
    cornerlist = []
    worstlist = []
    badlist = []
    neutralist = []
    ordered = []

    corners = [(0,0),(0,7),(7,0),(7,7)]
    worst = [(1,1),(1,6),(6,1),(6,6)]
    bad = [(0,1),(1,0),(1,7),(0,6),(7,1),(6,0),(7,6),(6,7)]
    for m in moves:
        if (m) in corners:
            cornerlist.insert(0, m)  
        elif (m) in bad:
            badlist.append(m)
        elif (m) in worst:
            worstlist.append(m)      
        else:
            neutralist.append(m)
    ordered.extend(cornerlist)
    ordered.extend(neutralist)
    ordered.extend(badlist)
    ordered.extend(worstlist)

    return ordered
