from language_model import LanguageModel

import pytest

good_phrases = ["toki", "a", "mi pona", "sina sona ala sona e toki pona?"]
bad_phrases = ["tau popolam", "betonomeshalka"]


@pytest.mark.parametrize('good_phrase', good_phrases)
@pytest.mark.parametrize('bad_phrase', bad_phrases)
def test_language_model_perplexity(good_phrase, bad_phrase):
    lm = LanguageModel()
    good_score = lm.score_sentence(good_phrase)
    bad_score = lm.score_sentence(bad_phrase)
    assert good_score < bad_score
