import gzip
from importlib.resources import files


all_words = []

with files("fwordlesolver.data").joinpath("sowpods.txt.gz").open("rb") as fo:
    file = gzip.decompress(fo.read())
    all_words = file.decode("utf-8").splitlines()


__all__ = ["all_words"]
