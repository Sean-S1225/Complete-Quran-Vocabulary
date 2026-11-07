import pandas as pd

conversionTable = {
    # Arabic letters
    "'": "\u0621",  # ء HAMZA
    ">": "\u0623",  # أ ALEF WITH HAMZA ABOVE
    "&": "\u0624",  # ؤ WAW WITH HAMZA ABOVE
    "<": "\u0625",  # إ ALEF WITH HAMZA BELOW
    "}": "\u0626",  # ئ YEH WITH HAMZA ABOVE
    "A": "\u0627",  # ا ALEF
    "b": "\u0628",  # ب
    "p": "\u0629",  # ة TA MARBUTA
    "t": "\u062A",  # ت
    "v": "\u062B",  # ث
    "j": "\u062C",  # ج
    "H": "\u062D",  # ح
    "x": "\u062E",  # خ
    "d": "\u062F",  # د
    "*": "\u0630",  # ذ
    "r": "\u0631",  # ر
    "z": "\u0632",  # ز
    "s": "\u0633",  # س
    "$": "\u0634",  # ش
    "S": "\u0635",  # ص
    "D": "\u0636",  # ض
    "T": "\u0637",  # ط
    "Z": "\u0638",  # ظ
    "E": "\u0639",  # ع
    "g": "\u063A",  # غ
    "_": "\u0640",  # ـ TATWEEL
    "f": "\u0641",  # ف
    "q": "\u0642",  # ق
    "k": "\u0643",  # ك
    "l": "\u0644",  # ل
    "m": "\u0645",  # م
    "n": "\u0646",  # ن
    "h": "\u0647",  # ه
    "w": "\u0648",  # و
    "Y": "\u0649",  # ى ALEF MAKSURA
    "y": "\u064A",  # ي

    # Harakat / diacritics
    "F": "\u064B",  # ً FATHATAN
    "N": "\u064C",  # ٌ DAMMATAN
    "K": "\u064D",  # ٍ KASRATAN
    "a": "\u064E",  # َ FATHA
    "u": "\u064F",  # ُ DAMMA
    "i": "\u0650",  # ِ KASRA
    "~": "\u0651",  # ّ SHADDA
    "o": "\u0652",  # ْ SUKUN

    # Qur'anic / extended Buckwalter characters
    "^": "\u0653",  # ٓ MADDAH ABOVE
    "#": "\u0654",  # ٔ HAMZA ABOVE
    "`": "\u0670",  # ٰ SUPERSCRIPT ALEF
    "{": "\u0671",  # ٱ ALEF WASLA

    ":": "\u06DC",  # ۜ SMALL HIGH SEEN
    "@": "\u06DF",  # ۟ SMALL HIGH ROUNDED ZERO
    '"': "\u06E0",  # ۠ SMALL HIGH UPRIGHT RECTANGULAR ZERO
    "[": "\u06E2",  # ۢ SMALL HIGH MEEM ISOLATED FORM
    ";": "\u06E3",  # ۣ SMALL LOW SEEN
    ",": "\u06E5",  # ۥ SMALL WAW
    ".": "\u06E6",  # ۦ SMALL YEH
    "!": "\u06E8",  # ۨ SMALL HIGH NOON
    "-": "\u06EA",  # ۪ EMPTY CENTRE LOW STOP
    "+": "\u06EB",  # ۫ EMPTY CENTRE HIGH STOP
    "%": "\u06EC",  # ۬ ROUNDED HIGH STOP WITH FILLED CENTRE
    "]": "\u06ED",  # ۭ SMALL LOW MEEM

    # Standard Buckwalter ALEF WITH MADDA.
    # QAC notes this isn't used in the Tanzil XML/JQuranTree encoding,
    # but retaining it makes the converter more complete.
    "|": "\u0622",  # آ

    " ": " ",
}


def convert_buckwalter_to_arabic(s):
    return "".join(conversionTable[x] for x in s)

def split_and_convert(x):

    d = {

    }

    toReturn = []
    temp = x.split("|")
    for y in temp:
        if "LEM:" in y:
            toReturn.append()


database = pd.read_csv(
    "./quranic-corpus-morphology-0.4.txt",
    skiprows=57,
    sep="\t",
    header=None,
    keep_default_na=False
)

database.columns = ["Position", "ArabicBuckwalter", "POS", "Morphology"]

database["Arabic"] = database["ArabicBuckwalter"].apply(
    convert_buckwalter_to_arabic
)

# print(set(database["Morphology"].apply(lambda x: x.split("|")[0]).to_list()))

# 3 types of tags: 'PREFIX', 'SUFFIX', 'STEM'

print(database["Morphology"].apply(lambda x: x.split("|")))

# print(database["Morphology"].apply(lambda x: x.split("|")))