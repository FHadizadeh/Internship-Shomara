import re


class PersianNormalizer:
    def __init__(self):

        self.switcher = {
            'ALEF': '\u0627',
            'ALEF_MADDA': '\u0622',
            'ALEF_HAMZA_ABOVE': '\u0623',
            'ALEF_HAMZA_BELOW': '\u0625',

            'WAW': '\u0648',
            'WAW_HAMZA_ABOVE': '\u0624',

            'YEH': '\u064A',
            'YEH_HAMZA_ABOVE': '\u0626',
            'FARSI_YEH': '\u06CC',

            'KAF': '\u0643',
            'KEHEH': '\u06A9',

            'HEH': '\u0647',
            'HEH_HAMZA_ABOVE': '\u06C2',
            'TEH_MARBUTA': '\u0629',

            'KASHIDA': '\u0640',

            'HAMZA': '\u0621',

            'FATHATAN': '\u064B',
            'DAMMATAN': '\u064C',
            'KASRATAN': '\u064D',
            'FATHA': '\u064E',
            'DAMMA': '\u064F',
            'KASRA': '\u0650',
            'SHADDA': '\u0651',
            'SUKUN': '\u0652'
        }

        self.switche = {}
        for (k, v) in self.switcher.items():
            v_new = v
            if k in ['ALEF_MADDA', 'ALEF_HAMZA_ABOVE', 'ALEF_HAMZA_BELOW']:
                v_new = self.switcher['ALEF']
            elif k in ['WAW_HAMZA_ABOVE']:
                v_new = self.switcher['WAW']
            elif k in ['YEH', 'YEH_HAMZA_ABOVE']:
                v_new = self.switcher['FARSI_YEH']
            elif k in ['KAF']:
                v_new = self.switcher['KEHEH']
            elif k in ['TEH_MARBUTA', 'HEH_HAMZA_ABOVE']:
                v_new = self.switcher['HEH']
            elif k in ['KASHIDA', 'KASRATAN', 'DAMMATAN', 'FATHATAN', 'FATHA', 'DAMMA', 'KASRA', 'SHADDA', 'SUKUN',
                       'HAMZA']:
                v_new = ''
            self.switche[v] = v_new

    def normalize(self, text):

        stringBuilder = ""
        for i in range(len(text)):
            if text[i] in self.switche.keys():
                stringBuilder += self.switche.get(text[i])
            else:
                stringBuilder += text[i]

        return stringBuilder


synonyms = {
    'خ': 'خیابان',
    'خیابان': 'خیابان',
    'ک': 'کوچه',
    'کوچه': 'کوچه',
    'ب': 'بلوار',
    'بلوار': 'بلوار',
    'بل': 'بلوار',
    'پ': 'پلاک',
    'پلاک': 'پلاک',
    'م': 'میدان',
    'میدان': 'میدان',
    'بن': 'بن‌بست',
    'بن‌بست': 'بن‌بست',
    'بن بست': 'بن‌بست',
    'ط': 'طبقه',
    'طبقه': 'طبقه'
}


def partition(arr, split_char):
    res = []
    for s in arr:
        s = s.strip()
        if s == '':
            continue
        s1 = []
        k = s.find(split_char)
        s2 = ''
        while k != -1:
            flag = True
            if k > 0 and (ord('ی') >= ord(s[k - 1]) >= ord('ا')):
                flag = False
            if k + len(split_char) < len(s) and (
                    ord('ی') >= ord(s[k + len(split_char)]) >= ord('ا')):
                flag = False
            if flag:
                s2 += s[:k]
                if s2 != '':
                    s1.append(s2)
                s2 = synonyms[split_char]
            else:
                s2 += s[:k + len(split_char)]
            s = s[k + len(split_char):]
            k = s.find(split_char)
        s2 += s
        if s2 != '':
            s1.append(s2)
        res += s1

    return res


def normalize(s):
    #     res = re.sub(r'[^\w\s]', ' ', s)
    res = PersianNormalizer().normalize(s)
    res = re.sub(r'[.]', ' ', res)
    res = re.split('[-ـ_,/،]', res)
    for i in synonyms.keys():
        res = partition(res, i)
    res_address = ''
    for r in res:
        res_address += r
        res_address += '، '
    return res_address[:len(res_address)-2]
