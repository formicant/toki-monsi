import re
import sys
from typing import List

from nltk.lm import Laplace
from nltk.lm.preprocessing import padded_everygram_pipeline, pad_both_ends
from nltk.util import everygrams

from corpus import get_valid_sentences


class LanguageModel:
    def __init__(self, ngram_order: int = 2):
        self.ngram_order = ngram_order
        self.lm = self.get_lm_model()

    @staticmethod
    def tokenize(sentence: str) -> List[str]:
        """
        This function replaces all first-capital words with a `PROPER_NOUN` tag.
        I thought it would make sense during fitting because the training corpus
        contains some proper nouns. Feel free to remove this, though.
        """
        tokens = re.findall(r'\w+', sentence)
        tokens = ["PROPER_NOUN" if x[0].isupper() else x for x in tokens]
        return tokens

    def get_lm_model(self) -> Laplace:
        sents = [self.tokenize(sentence) for sentence in get_valid_sentences()]
        train, vocab = padded_everygram_pipeline(self.ngram_order, sents)
        train = [list(x) for x in train]
        vocab = list(vocab)
        lm = Laplace(2)
        lm.fit(train, vocab)
        return lm

    def score_sentence(self, sentence: str) -> float:
        tokens = self.tokenize(sentence)
        bigram_padded_tokens = everygrams(pad_both_ends(
            tokens, n=self.ngram_order))
        return self.lm.entropy(bigram_padded_tokens)


def main():
    lm = LanguageModel()
    print(lm.score_sentence(sys.argv[1]))


if __name__ == '__main__':
    main()
