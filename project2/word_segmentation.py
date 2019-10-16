# Copyright (c) 2019 Yan Wang.All rights reserved.
# date : 2019/10/7
# auther : Yan Wang<dieqi317@gmail.com>
# file : word_segmentation.py

############################################################################################
# txt file dir
############################################################################################
dic_file_dir = './data/dic_ec.txt'


############################################################################################
# some utils
############################################################################################
# get the dic from dic_file
# the dic  contains all the Chinese words in the .txt file.
def get_chinese_dict(path):
    dict_list = []
    fd = open(path, 'r')
    i = 1
    for line in fd.readlines():
        temp = []
        lineVec = str(line).strip().split('')
        for temp_line in lineVec:
            if (',' in temp_line) :
                chinese_word = temp_line.strip().split(', ')
                for temp in chinese_word :
                    dict_list.append(temp)
    return dict_list

# change the word_list to word_str
def get_str(word_list):
    word_str = ''
    for inst in word_list:
        word_str += (inst + '  ')
    return word_str


############################################################################################
# FMM and RMM
############################################################################################
# use Forward Maximum Matching to realize chinese word segmentation
def FMM(sentence , dic , max_chars = 6):
    len_sent = len(sentence)
    segmentation_result = []
    pointer = 0

    while pointer < len_sent :
        # get the max_len word
        if (pointer + max_chars < len_sent):
            temp_word = sentence[pointer : pointer + max_chars]
        else:
            temp_word = sentence[pointer :]
        # segmente one word
        while len(temp_word) > 0 :
            if (temp_word in dic and len(temp_word) > 1):
                segmentation_result.append(temp_word)
                pointer = pointer + len(temp_word)
                break
            elif (len(temp_word) == 1) :
                segmentation_result.append(temp_word)
                pointer = pointer + len(temp_word)
                break
            else:
                temp_word = temp_word[:-1]

    return segmentation_result

# use Reverse Maximum Matching to realize chinese word segmentation
def RMM(sentence , dic , max_chars = 6):
    len_sent = len(sentence)
    segmentation_result = []
    pointer = len_sent

    while pointer > 0 :
        # get the max_len word
        if (pointer - max_chars >= 0):
            temp_word = sentence[pointer - max_chars : pointer]
        else:
            temp_word = sentence[: pointer]
        # segmente one word
        while len(temp_word) > 0 :
            if (temp_word in dic and len(temp_word) > 1):
                segmentation_result.append(temp_word)
                pointer = pointer - len(temp_word)
                break
            elif (len(temp_word) == 1) :
                segmentation_result.append(temp_word)
                pointer = pointer - len(temp_word)
                break
            else:
                temp_word = temp_word[1:]

    segmentation_result = segmentation_result[::-1]
    return segmentation_result

# print the result of word segmentation
def result_print(sentence , FMM_result , RMM_result):
    print ('the test sentence is : ' + sentence)
    print ('the FMM result is : ' + get_str(FMM_result))
    print ('the RMM result is : ' + get_str(RMM_result))


############################################################################################
# main()
############################################################################################
def main():
    test_sentence = '乒乓球拍卖完了。'
    test_sentence_2 = '今天是个好日子。'
    dict_used = get_chinese_dict(dic_file_dir)
    FMM_result = FMM(test_sentence , dict_used)
    RMM_result = RMM(test_sentence , dict_used)

    result_print(test_sentence , FMM_result ,RMM_result)

if __name__ == '__main__':
    main()
