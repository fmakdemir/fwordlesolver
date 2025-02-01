from wordlesolver.matcher import match


def test_matches():
    assert match("brighter", "arabised") == "?x?...x."
    assert match("alabired", "brighter") == "...???x."
    assert match("alrbirer", "brighter") == "..???.xx"
    assert match("alrbired", "brighter") == "..????x."
    assert match("achy", "hast") == "?.?."
