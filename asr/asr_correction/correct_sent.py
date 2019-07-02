# !/usr/bin/env python3

import pypinyin
import editdistance

letters = 'abcdefghijklmnopgrstuvwxyz'
tone = '1234'

def replace_suspect_word_to_sentence(word, sent, dis=1):
    sent_pinyin = pypinyin.pinyin(sent, style=pypinyin.TONE3)
    sent_pinyin = [i[0][:-1] if i[0][-1] in tone else i[0] for i in sent_pinyin]
    sent_chars = list(sent)
    word_pinyin = pypinyin.pinyin(word, style=pypinyin.TONE3)
    word_pinyin = [i[0][:-1] if i[0][-1] in tone else i[0] for i in word_pinyin]
    word_len = len(word_pinyin)
    sent_len = len(sent_pinyin)
    replace_pos = []
    for i in range(sent_len-word_len+1):
        sent_word = sent_pinyin[i:i+word_len]
        for s in sent_word:
            if len(s) == 0:
                break
            if len(s) == 1:
                if s not in letters:
                    break
        sent_word_edit = ''.join(sent_word)
        word_edit = ''.join(word_pinyin)
        if editdistance.distance(sent_word_edit, word_edit) <= dis:
            replace_pos.append(i)
    for pos in replace_pos:
        sent_chars[pos:pos+word_len] = word
    res = ''.join(sent_chars)
    return res


if __name__ == '__main__':
    a = '你好，我是希格斯的里头'
    b = '猎头'
    res = replace_suspect_word_to_sentence(b, a)
    print(res)
    print('hello world!')