import re
from parsita import TextParsers, Parser, Success
from parsita import lit, reg, opt, rep, rep1, repsep, rep1sep, first, longest, pred

class TokiPonaGrammar:
    def __init__(self, word_list: list[str]):
        word_boundary = reg(re.compile(r'\b\W*'))
        
        def word(w: str) -> Parser[str, str]:
            return lit(w) << word_boundary
        
        def any_of_words(*ws: str) -> Parser[str, str]:
            words = [word(w) for w in ws]
            return first(*words)
        
        def is_not_pronoun(subject_phrase_result):
            return subject_phrase_result not in [[[['mi', []]]], [[['sina', []]]]]  # oh god!
        
        grammatical_words = { 'a', 'anu', 'e', 'en', 'kin', 'la', 'li', 'o', 'pi' }
        
        content_words = [w for w in word_list if w not in grammatical_words]
        
        class TokiPonaParser(TextParsers, whitespace=None):
            
            # word categories
            
            content_word = any_of_words(*content_words)
            
            proper_noun = reg(re.compile(
                r'''( (?!Ji|Ti|Wo|Wu)[JKLMNPSTW][aeiou] | [AEIOU] ) (?!nn)n?
                    ( (?!ji|ti|wo|wu)[jklmnpstw][aeiou] (?!nn)n? )*
                    \b\W*
                ''', flags=re.VERBOSE))
            
            # noun phrase
            
            modifier = longest(
                word('pi') & content_word & rep1(modifier),
                any_of_words('kin', 'a'),
                proper_noun,
                content_word
            )
            
            noun_phrase = rep1sep(content_word & rep(modifier), word('anu'))
            
            subject_phrase = rep1sep(noun_phrase, word('en'))
            
            # verb phrase
            
            direct_object = word('e') & noun_phrase
            
            verb_phrase = noun_phrase & rep(direct_object)
            
            # sentence
            
            context_or_main_phrase = longest(
                any_of_words('mi', 'sina') & verb_phrase,
                word('nimi') & opt(modifier) & rep1(word('li') & (proper_noun | verb_phrase)),
                pred(subject_phrase, is_not_pronoun, 'non-pronoun subject') & rep1(word('li') & verb_phrase),
                subject_phrase
            )
            
            context_phrase = longest(
                any_of_words('anu', 'kin'),
                context_or_main_phrase
            )
            
            main_phrase = longest(
                rep1(word('a')),
                opt(subject_phrase) & word('o') & repsep(verb_phrase, word('o')),
                context_or_main_phrase
            )
            
            sentence = longest(
                rep(context_phrase & word('la')) & main_phrase,
                word('taso') & sentence
            )
        
        self.parser = TokiPonaParser


    def is_valid(self, sentence: str) -> bool:
        result = self.parser.sentence.parse(sentence)
        return isinstance(result, Success)
