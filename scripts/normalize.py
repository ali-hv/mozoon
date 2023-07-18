import re

def normalize(line): # source: https://github.com/amnghd/Persian_poems_corpus/blob/master/pers_alphab.py
    """
    This function removes all the elements that are in a Persian
    literature that is not a part of a normal alphabet.    
    """
   
    space_pattern = r"[\xad\ufeff\u200e\u200d\u200b\x7f\u202a\u2003\xa0\u206e\u200c\x9d]"
    space_pattern = re.compile(space_pattern)

    line = space_pattern.sub(" ", line)
    

    deleted_pattern = r"(|[\|\[]]|\"|'ٍ¬|[a-zA-Z]|[؛“،”‘۔’’‘–]|[|\.÷+\:\-\?»\=\{}\*«_…\؟!ـ]|[۲۹۱۷۸۵۶۴۴۳]|[\\u\\x]|[\(\)]|[۰'ٓ۫'ٔ]|[ٓٔ]|[ًٌٍْﹼ،َُِّ«ٰ»ٖء]|\[]|\[\])"
    deleted_pattern = re.compile(deleted_pattern)

    line = deleted_pattern.sub("", line)

    letter_dict = dict()

    letter_dict[u"ۀ"] = u"ه"

    letter_dict[u"ة"] = u"ت"

    letter_dict[u"ي"] = u"ی"

    letter_dict[u"ؤ"] = u"و"

    letter_dict[u"إ"] = u"ا"

    letter_dict[u"ٹ"] = u"ت"

    letter_dict[u"ڈ"] = u"د"

    letter_dict[u"ئ"] = u"ی"

    letter_dict[u"ﻨ"] = u"ن"

    letter_dict[u"ﺠ"] = u"ج"

    letter_dict[u"ﻣ"] = u"م"

    letter_dict[u"ﷲ"] = u""

    letter_dict[u"ﻳ"] = u"ی"

    letter_dict[u"ٻ"] = u"ب"

    letter_dict[u"ٱ"] = u"ا"

    letter_dict[u"ڵ"] = u"ل"

    letter_dict[u"ﭘ"] = u"پ"

    letter_dict[u"ﻪ"] = u"ه"

    letter_dict[u"ﻳ"] = u"ی"

    letter_dict[u"ٻ"] = u"ب"

    letter_dict[u"ں"] = u"ن"

    letter_dict[u"ٶ"] = u"و"

    letter_dict[u"ٲ"] = u"ا"

    letter_dict[u"ہ"] = u"ه"

    letter_dict[u"ﻩ"] = u"ه"

    letter_dict[u"ﻩ"] = u"ه"

    letter_dict[u"ك"] = u"ک"

    letter_dict[u"ﺆ"] = u"و"

    letter_dict[u"أ"] = u"ا"

    letter_dict[u"ﺪ"] = u"د"
    

    letter_pattern = re.compile(r"(" + "|".join(letter_dict.keys()) + r")")

    line = letter_pattern.sub(lambda x: letter_dict[x.group()], line) 
    
    return line