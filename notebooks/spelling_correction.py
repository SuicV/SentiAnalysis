import re
from spellchecker import SpellChecker
def spelling_correction(__reviews):
    """
    correct misspelled words from reviews. this methode use SpellChecker package.
    check documentation of SpellChecker in this link https://pyspellchecker.readthedocs.io/en/latest/

    :return: None
    """
    spell_checker = SpellChecker()
    for index, review in __reviews.items():
        print(f"threating reaview with index {index}")
        words = re.findall(r"[\w']+", review)
        for word in words:
            if len(word) > 2:
                correction = spell_checker.correction(word)
                review = review.replace(word, correction)
        __reviews[index] = review
    return __reviews