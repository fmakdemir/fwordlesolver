import pytest

from wordlesolver.solver import Solver


def test_solver():
    COUNT = 6
    solver = Solver(COUNT)

    sugg = solver.get_suggestions()
    assert len(sugg) == 5
    assert all(len(w) == COUNT for w in sugg)

    with pytest.raises(TypeError):
        solver.filter_word("brighter", "x?...x")

    # target is bright
    # mark 2 characters as found
    solver.filter_word("basket", "x....x")
    assert len(solver.words) > 1
    assert all(w[0] == "b" and w[-1] == "t" for w in solver.words)

    # mark 2 more characters as found
    solver.filter_word("..gi..", "..??..")
    assert "bright" in solver.words
    assert all("g" in w and "i" in w for w in solver.words)

    # mark last 2 characters as found
    solver.filter_word(".r.g..", ".x.x..")
    assert len(solver.words) == 1
    assert solver.words[0] == "bright"


def test_solver_score():
    COUNT = 3
    solver = Solver(COUNT)
    solver.words = ["abc", "aba", "bad", "ced", "abe", "zen"]
    scores = [12, 8, 12, 14, 14, 10]

    solver.update_char_cnts()

    for w, s in zip(solver.words, scores):
        assert solver.get_score(w) == s

    sugg = solver.get_suggestions()
    assert sugg == ["abe", "ced", "bad", "abc", "zen"]
