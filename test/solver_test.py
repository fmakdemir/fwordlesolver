import pytest

from fwordlesolver.solver import WordleSolver


def test_solver():
    COUNT = 6
    solver = WordleSolver(COUNT)

    sugg = solver.get_suggestions()
    assert len(sugg) == 5
    assert all(len(w) == COUNT for w in sugg)

    with pytest.raises(TypeError):
        solver.apply_guess("brighter", "x?...x")

    # target is bright
    # mark 2 characters as found
    solver.apply_guess("basket", "x....x")
    assert len(solver.words) > 1
    assert all(w[0] == "b" and w[-1] == "t" for w in solver.words)

    # mark 2 more characters as found
    solver.apply_guess("..gi..", "..??..")
    assert "bright" in solver.words
    assert all("g" in w and "i" in w for w in solver.words)

    # mark last 2 characters as found
    solver.apply_guess(".r.g..", ".x.x..")
    assert len(solver.words) == 1
    assert solver.words[0] == "bright"


def test_solver_score():
    COUNT = 3
    solver = WordleSolver(COUNT)
    solver.words = ["abc", "aba", "bad", "ced", "abe", "zen"]
    expected_scores = [12, 8, 12, 14, 14, 10]

    # trigger score pre-calculation
    solver.get_suggestions(len(solver.words))

    for w, s in zip(solver.words, expected_scores):
        assert solver.get_score(w) == s

    sugg = solver.get_suggestions()
    assert sugg == ["abe", "ced", "bad", "abc", "zen"]


def test_solver_used_letters():
    COUNT = 5
    solver = WordleSolver(COUNT)
    solver.apply_guess("abcde", "xxxxx")
    assert solver.used_letters == set("abcde")
    solver.apply_guess("abfgh", "xxxxx")
    assert solver.used_letters == set("abcdefgh")
    solver.apply_guess("cvced", "xxxxx")
    assert solver.used_letters == set("abcdefghv")

    sugg = solver.get_not_used_suggestion()
    print(sugg)
    for s in sugg:
        assert not any(c in solver.used_letters for c in s)
