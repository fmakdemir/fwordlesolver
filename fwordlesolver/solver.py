from collections import defaultdict

from .data import all_words


class WordleSolver:
    def __init__(self, word_size: int):
        self.word_size = word_size
        self.words = [w for w in all_words if len(w) == word_size]
        self.used_letters = set()
        self.not_used_words = [*self.words]

    @property
    def len_words(self):
        return len(self.words)

    def get_score(self, word):
        return sum(
            self.len_words - abs(2 * self.char_cnts[c] - self.len_words)
            for c in set(word)
        )

    def get_suggestions(self, n=5):
        """Returns the 5 words with the highest score"""
        self.char_cnts = defaultdict(int)
        for w in self.words:
            for c in set(w):
                self.char_cnts[c] += 1

        return sorted(self.words, key=self.get_score)[-n:][::-1]

    def get_not_used_suggestion(self):
        """Returns the 5 words with words not guessed letters"""
        return sorted(self.not_used_words, key=lambda k: len(set(k)))[-5:][::-1]

    def filter_words(self, check_func: lambda x: bool):
        self.words = [w for w in self.words if check_func(w)]

    def validate_inputs(self, word: str, places: str):
        if len(word) != self.word_size or len(places) != self.word_size:
            raise TypeError(f"Invalid input length, expected {self.word_size}")
        for p in places:
            if p not in "x.?":
                raise TypeError(f"Invalid placement character: {p}")

    def apply_guess(self, word: str, places: str):
        word = word.strip().lower()
        places = places.strip().lower()

        self.validate_inputs(word, places)

        self.used_letters.update(set(word))
        self.not_used_words = [
            w for w in self.not_used_words if not self.used_letters.intersection(set(w))
        ]

        for i, (c, p) in enumerate(zip(word, places)):
            # len_words = len(self.words)
            if p == "x":
                self.filter_words(lambda w: w[i] == c)
            if p == "?":
                self.filter_words(lambda w: w[i] != c and c in w)
            if p == ".":
                hits = sum(1 for (_c, _p) in zip(word, places) if _p != "." and _c == c)
                self.filter_words(lambda w: w.count(c) <= hits)
            # print(f"Filtered {c}{p} from {len_words} to {len(self.words)}")
        # print("-" * 20)
        # print(self.words)
        # print("-" * 20)
