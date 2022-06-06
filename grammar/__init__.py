import re
from parsita import TextParsers, Parser, Success
from parsita import lit, reg, opt, rep, rep1, repsep, rep1sep, first, longest, pred, success

def is_valid(sentence: str) -> bool:
    result = TokiPonaParsers.sentence.parse(sentence)
    return isinstance(result, Success)


word_boundary = reg(re.compile(r'\b[^A-Za-z]*'))

def word(w: str) -> Parser[str, str]:
    return lit(w) << word_boundary

def any_of_words(*ws: str) -> Parser[str, str]:
    words = [word(w) for w in ws]
    return first(*words)

def is_not_pronoun(subject_phrase_result):
    return subject_phrase_result not in [[[['mi', []]]], [[['sina', []]]]]  # oh god!


class TokiPonaParsers(TextParsers, whitespace=None):
    
    # word categories
    
    preposition  = any_of_words('lon', 'tawa', 'tan', 'kepeken', 'sama')
    
    content_word = any_of_words(
        'akesi',   'ala',     'alasa',   'ale',     'ali',     'anpa',
        'ante',    'awen',    'esun',    'ijo',     'ike',     'ilo',
        'insa',    'jaki',    'jan',     'jelo',    'jo',      'kala',
        'kalama',  'kama',    'kasi',    'ken',     'kepeken', 'kili',
        'kiwen',   'ko',      'kon',     'kule',    'kulupu',  'kute',
        'lape',    'laso',    'lawa',    'len',     'lete',    'lili',
        'linja',   'lipu',    'loje',    'lon',     'luka',    'lukin',
        'lupa',    'ma',      'mama',    'mani',    'meli',    'mi',
        'mije',    'moku',    'moli',    'monsi',   'mu',      'mun',
        'musi',    'mute',    'namako',  'nanpa',   'nasa',    'nasin',
        'nena',    'ni',      'nimi',    'noka',    'oko',     'olin',
        'ona',     'open',    'pakala',  'pali',    'palisa',  'pan',
        'pana',    'pilin',   'pimeja',  'pini',    'pipi',    'poka',
        'poki',    'pona',    'pu',      'sama',    'seli',    'selo',
        'seme',    'sewi',    'sijelo',  'sike',    'sin',     'sina',
        'sinpin',  'sitelen', 'sona',    'soweli',  'suli',    'suno',
        'supa',    'suwi',    'tan',     'taso',    'tawa',    'telo',
        'tenpo',   'toki',    'tomo',    'tu',      'unpa',    'uta',
        'utala',   'walo',    'wan',     'waso',    'wawa',    'weka',
        'wile')
    
    proper_noun = reg(re.compile(
        r'''( (?!Ji|Ti|Wo|Wu)[JKLMNPSTW][aeiou] | [AEIOU] ) (?!nn)n?
            ( (?!ji|ti|wo|wu)[jklmnpstw][aeiou] (?!nn)n? )*
            \b[^A-Za-z]*
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
    
    context_phrase = longest(
        any_of_words('anu', 'kin'),
        any_of_words('mi', 'sina') & verb_phrase,
        pred(subject_phrase, is_not_pronoun, 'non-pronoun subject') & rep1(word('li') & verb_phrase),
        subject_phrase
    ) & word('la')
    
    main_phrase = longest(
        rep1(word('a')),
        any_of_words('mi', 'sina') & verb_phrase,
        pred(subject_phrase, is_not_pronoun, 'non-pronoun subject') & rep1(word('li') & verb_phrase),
        opt(subject_phrase) & word('o') & repsep(verb_phrase, word('o')),
        subject_phrase
    )
    
    sentence = rep(context_phrase) & main_phrase


if __name__ == '__main__':
    sentence = 'jan Mosima o, ni li soweli sina anu seme'
    parser = TokiPonaParsers.sentence
    result = parser.parse(sentence).or_die()
    print(result)
