import re
from unidecode import unidecode

NEWLINE_PATTERN = "(\\n)"
PUNCTUATION_PATTERN = "[\u0021-\u0026\u0028-\u002F\u003A-\u003F\u005B-\u005F\u2010-\u2028\ufeff]+" #keeps apostrophe


TAG_PATTERN = re.compile(r"\[.*?\]")
ALTERNATIVE_TAG_PATTERN = re.compile(
    r"(?im)^(verse|chorus|intro|outro|bridge|pre-chorus|hook|interlude)\b.*?:"
)
REPEAT_MARKER_PATTERN = re.compile(r"\(\s*x\s*\d+\s*\)", flags=re.IGNORECASE)
GENIUS_BOILERPLATE_PATTERNS = [
    re.compile(r"^\d+\s*Contributors?.*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*?Lyrics\s*$", re.MULTILINE) ,  # "SongTitle Lyrics" header line
    re.compile(r"\bEmbed\b", re.IGNORECASE),
    re.compile(r"You might also like", re.IGNORECASE),
    re.compile(r"^\d+$", re.MULTILINE),  # stray view-count lines
]
LRC_TIMESTAMP_PATTERN = re.compile(r"\[\d{2}:\d{2}(?:\.\d{2,3})?\]")


def strip_boilerplate(text: str) -> str:
    text = LRC_TIMESTAMP_PATTERN.sub("", text)
    text = REPEAT_MARKER_PATTERN.sub("", text)      # do this BEFORE stripping tags/punct
    text = TAG_PATTERN.sub("", text)
    text = ALTERNATIVE_TAG_PATTERN.sub("", text)
    for pat in GENIUS_BOILERPLATE_PATTERNS:
        text = pat.sub("", text)
    return text



def regex_cleaner(raw_text, 
            no_newlines = True,
            no_punctuation = True,
            no_boilerplate = True,
            ):
    """Clean a raw text with regular expressions and return the cleaned string."""


    clean_text = raw_text

    censored_dict = {
        r'\bb\w*\*+\w*h\b': 'bitch',
        r'\bf\w*\*+\w*k\b': 'fuck',
        r'\bs\w*\*+\w*t\b': 'shit',
        r'\ba\w*\*+\w*s\b': 'ass',
        r'\bn\w*\*+\w*a\b': 'nigga'
    }
    
    for pattern, replacement in censored_dict.items():
        clean_text = re.sub(pattern, replacement, clean_text, flags=re.IGNORECASE)

    if no_boilerplate:
            clean_text = strip_boilerplate(clean_text)

    if no_newlines:
                clean_text = re.sub(NEWLINE_PATTERN," ",clean_text)
    
    if no_punctuation:
        clean_text = re.sub(PUNCTUATION_PATTERN,"",clean_text)    


    #clean_text = re.sub(r'[^a-zA-Z0-9\s\'-]', '', clean_text)
    
    #Clean up extra spaces left behind by deleted punctuation
    
    clean_text = re.sub(r'\s+', ' ', clean_text)

    
    return clean_text



def preprocess_text(raw_text, lowercase = True, strip = True, regex_clean = True,unicode_remove = True, **kwargs):

    """
    this function has the purpose of cleaning text data
    to perform EDA

    it does the following:
    
    -normalizes words by putting all of them into lower case
    -removes uninmportant characters such as '\n'
    -removes unecessary white spaces~
    -removes punctuation
    -removes emojis, 
    -removes song structural tags
    -removes diacritics, homoglyphs and other unicode errors
    """

    text = raw_text

    if unicode_remove:                #unidecode is a function that tries to convert unicode characters into the closest ascii equivalent 
        text = unidecode(text)        #if a character does not have any match it simply is deleted e.g. (emojis)

    if regex_clean:
        text = regex_cleaner(text)
        
    if lowercase:
        text = text.lower()
    


    return text


