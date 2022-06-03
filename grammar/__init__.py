import re
from parsita import TextParsers, Parser, Success
from parsita import lit, reg, opt, rep, rep1, repsep, rep1sep, first, pred

def is_valid(sentence: str) -> bool:
    result = TokiPonaParsers.sentence.parse(sentence)
    return isinstance(result, Success)


word_boundary = reg(re.compile(r'\b[^A-Za-z]*'))

def word(w: str) -> Parser[str, str]:
    return lit(w) << word_boundary

def any_of_words(*ws: str) -> Parser[str, str]:
    words = [word(w) for w in ws]
    return first(*words)


class TokiPonaParsers(TextParsers, whitespace=None):
    # TODO: implement the grammar
    
    # word categories
    
    pronoun = any_of_words('mi', 'sina')
    
    content_word = any_of_words(
        'akesi',   'ala',     'alasa',   'ale',     'ali',     'anpa',
        'ante',    'awen',    'esun',    'ijo',     'ike',     'ilo',
        'insa',    'jaki',    'jan',     'jelo',    'jo',      'kala',
        'kalama',  'kama',    'kasi',    'ken',     'kepeken', 'kili',
        'kiwen',   'ko',      'kon',     'kule',    'kulupu',  'kute',
        'lape',    'laso',    'lawa',    'len',     'lete',    'lili',
        'linja',   'lipu',    'loje',    'lon',     'luka',    'lukin',
        'lupa',    'ma',      'mama',    'mani',    'meli',    'mije',
        'moku',    'moli',    'monsi',   'mu',      'mun',     'musi',
        'mute',    'namako',  'nanpa',   'nasa',    'nasin',   'nena',
        'ni',      'nimi',    'noka',    'oko',     'olin',    'ona',
        'open',    'pakala',  'pali',    'palisa',  'pan',     'pana',
        'pilin',   'pimeja',  'pini',    'pipi',    'poka',    'poki',
        'pona',    'pu',      'sama',    'seli',    'selo',    'seme',
        'sewi',    'sijelo',  'sike',    'sin',     'sinpin',  'sitelen',
        'sona',    'soweli',  'suli',    'suno',    'supa',    'suwi',
        'tan',     'taso',    'tawa',    'telo',    'tenpo',   'toki',
        'tomo',    'tu',      'unpa',    'uta',     'utala',   'walo',
        'wan',     'waso',    'wawa',    'weka',    'wile')

    proper_noun = reg(re.compile(
        r'''( (?!Ji|Ti|Wo|Wu)[JKLMNPSTW][aeiou] | [AEIOU] ) (?!nn)n?
            ( (?!ji|ti|wo|wu)[jklmnpstw][aeiou] (?!nn)n? )* \b
        ''', flags=re.VERBOSE))
    
    # numerals
    
    simple_numeral = any_of_words('wan', 'tu')
    numeral = word('tu') & simple_numeral | simple_numeral | word('luka') & opt(numeral)
    para_numeral = any_of_words('ala', 'mute', 'pini', 'kama')
    ordinal = word('nanpa') & (numeral | para_numeral)
    
    # debug
    
    non_content_word = any_of_words('a', 'anu', 'e', 'en', 'kin', 'la', 'li', 'o', 'pi')
    word = non_content_word | pronoun | content_word | proper_noun
    
    sentence = rep1(word)


if __name__ == '__main__':
    sentence = 'nanpa luka luka tu wan'
    result = TokiPonaParsers.ordinal.parse(sentence).or_die()
    print(result)
