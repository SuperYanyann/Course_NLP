# Copyright (c) 2019 Yan Wang.All rights reserved.
# date : 2019/10/7
# auther : Yan Wang<dieqi317@gmail.com>
# file : restore_words.py
'''
Attention :
1. replace the spaces by '|' in .txt
2 . try : sudo iconv -f 'latin1' -t 'utf-8' dic_ec.txt > dic_ec_u8.txt
'''
import nltk.stem as ns
import re

############################################################################################
# txt file dir
############################################################################################
dic_file_dir = './data/dic_ec.txt'

############################################################################################
# functions
############################################################################################
# get the dic from dic_file
# attention : the dic_file should be changed to 'utf-8'
def get_dict(path):
    dict_list = {}
    fd = open(path, 'r')
    for line in fd.readlines():
        temp = []
        lineVec = str(line).strip().split('')
        for content in lineVec[1:-1]:
            pattern = re.compile(r'([a-z]+).')
            if pattern.match(content):
                temp.append(content)
        dict_list[lineVec[0]] = temp

    return dict_list

# change the part_list to part_str
def get_str(part_list):
    part_str = ''
    for inst in part_list:
        part_str += (inst + '\t')
    return part_str


# search word in dic by nltk.stem
def search_word_use_nltk(word , dic):
    # restore words
    lemmatizer = ns.WordNetLemmatizer()
    n_lemma = lemmatizer.lemmatize(word, pos='n')
    v_lemma = lemmatizer.lemmatize(word, pos='v')
    # print('%s %s %s' %(word, n_lemma, v_lemma))

    # print result
    if word in dic.keys():
        print("Original form: " + word)
        part_str = get_str(dic[word])
        print ('The part of the word is : ' + part_str)
    elif n_lemma in dic.keys():
        print("Original form: " + n_lemma)
        part_str = get_str(dic[n_lemma])
        print ('The part of the word is : ' + part_str)
    elif v_lemma in dic.keys():
        print("Original form: " + v_lemma)
        part_str = get_str(dic[v_lemma])
        print ('The part of the word is : ' + part_str)
    else:
        print("There is no such word in the dictionary")
    print('------------------------')

# search word in dic by rule
def search_word_use_rule(word , dic):

    flag = False
    if word in dic.keys():
        print("Original form: " + word)
        part_str = get_str(dic[word])
        print('The part of the word is :' + part_str)
        flag = True
    # *ies -> *y (SINGULAR3)
    if not flag:
        if 'ies' == word[-3:len(word)]:
            tmp_word = word[0:-3]+'y'
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print('The part of the word is :' + part_str)
                flag = True
    # *es -> * (SINGULAR3)
    if not flag:
        if 'es' == word[-2:len(word)]:
            tmp_word = word[0:-2]
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *s -> * (SINGULAR3)
    if not flag:
        if 's' == word[-1:len(word)]:
            tmp_word = word[0:-1]
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *ing -> * (VING)
    if not flag:
        if 'ing' == word[-3:len(word)] and word[-4] == word[-5]:
            tmp_word = word[0:-4]
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *ying -> *ie (VING)
    if not flag:
        if 'ying' == word[-4:len(word)]:
            tmp_word = word[0:-4] + 'ie'
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *??ing -> *? (VING
    if not flag:
        if 'ing' == word[-3:len(word)]:
            if word[0:-3] in dic.keys():
                tmp_word = word[0:-3]
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
            elif word[0:-3]+'e' in dic.keys():
                tmp_word = word[0:-3]+'e'
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *ed -> * (PAST)(VEN)
    if not flag:
        if 'ed' == word[-2:len(word)] and word[-3]==word[-4]:
            tmp_word = word[0:-2] + word[-3]
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *ied -> *y (PAST)(VEN)
    if not flag:
        if 'ied' == word[-3:len(word)]:
            tmp_word = word[0:-3] + 'y'
            if tmp_word in dic.keys():
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    # *??ed -> *? (PAST)(VEN)
    if not flag:
        if 'ed' == word[-2:len(word)]:
            if word[0:-2] in dic.keys():
                tmp_word = word[0:-2]
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
            elif word[0:-2]+'e' in dic.keys():
                tmp_word = word[0:-2]+'e'
                print("Original form: " + tmp_word)
                part_str = get_str(dic[tmp_word])
                print("The part of the word is : " + part_str)
                flag = True
    if not flag:
        print("There is no such word in the dictionary")
    print('------------------------')


############################################################################################
# main()
############################################################################################
def main(search_mode):
    dict_used = get_dict(dic_file_dir)
    input_word = input("please input a word: ")

    # search word
    if search_mode == 'nltk':
        search_word_use_nltk(input_word , dict_used)
    elif search_mode == 'rule':
        search_word_use_rule(input_word , dict_used)

if __name__ == '__main__':
    while 1:
        main(search_mode = 'rule')
