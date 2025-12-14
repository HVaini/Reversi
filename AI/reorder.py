def reorder_moves(board, player, moves):
    """
    Esiluokittelee siirrot paremmuuden mukaan karkeilla kriteereillä
    Alpha-Beta-Karsinnan tehostamiseksi.
    Siirrot jotka johtavat kulman saamiseen ovat arvokkaimpia,
    siirrot jotka voivat johtaa kulman menetyksen ovat huonoimpia.

    :param board: pelilaudan tilanne
    :param player: vuorossa oleva pelaaja
    :param moves: lailliset siirrot pelaajalle
    :return: lista siirroista järjestettynä 
    """

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
