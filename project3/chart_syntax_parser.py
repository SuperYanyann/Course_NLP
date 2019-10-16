# Copyright (c) 2019 Yan Wang.All rights reserved.
# date : 2019/10/14 ~ 2019/10/16
# auther : Yan Wang<dieqi317@gmail.com>
# file : chart_syntax_parser.py
'''
e.g. : (0) the (1) cat (2) caught (3) a (4) mouse (5)
'''
import queue

############################################################################################
# txt file dir
############################################################################################
dic_file_dir = './data/dic.txt'
rule_file_dir = './data/rules.txt'
sentences_file_dir = './data/sentences.txt'


############################################################################################
# define some usefully class in chart parser
############################################################################################
# activateEdge :
class active_edge:
    def __init__(self,rule,break_point,begin_point,end_point):
        self.rule = rule
        self.break_point = break_point
        self.begin_point = begin_point
        self.end_point = end_point

# chart
class chart:
    def __init__(self,part,begin_point,end_point):
        self.part = part
        self.begin_point = begin_point
        self.end_point = end_point

# agenda_item :
class agenda_item:
    def __init__(self,part,begin_point,end_point):
        self.part = part
        self.begin_point = begin_point
        self.end_point = end_point

'''
# sentence :
class sentence:
    def __init__(self,words_string):
        self.string = words_string
'''

# rule :
# equalsign_left just have one part
# equalsign_right may have more then one part, so it's a list
class rule:
    def __init__(self,equalsign_left , equalsign_right):
        self.equalsign_left = equalsign_left
        self.equalsign_right = equalsign_right
        self.right_len = len(equalsign_right)

# define the important item in chart parser
run_point = 0 # the location _index which chart parser arives
active_edge_list = []
chart_list = []
rule_list = []
agenda = queue.Queue()


############################################################################################
# define some util functions
############################################################################################
# read sentences from txt file
def read_sentences(sentence_file):
    sentence_list = []
    with open(sentence_file,'r') as f:
        for line in f:
            sentence_list.append(list(line.strip('\n').split(' ')))
    f.close()
    return sentence_list

# get the dic of part from txt file
def get_dic(dic_file):
    dic = {}
    with open(dic_file,'r') as f:
        for line in f:
            temp = line.strip('\n').split('|')
            dic[temp[0]] = temp[1]
    f.close()
    return dic

# get all rule from txt file
def get_rules(rule_file):
    rule_list = []
    with open(rule_file,'r') as f:
        for line in f:
            temp = line.strip('\n').split(' ')
            temp_rule = rule(temp[0] , temp[2:])
            rule_list.append(temp_rule)
    f.close()
    return rule_list

# get relationship between opera_agenda and one rule
def get_rela_agenda2rules(agenda_item , rule):
    temp_part = agenda_item.part
    if (temp_part == rule.equalsign_right[0] and len(rule.equalsign_right) != 1):
        return 1
    elif (temp_part == rule.equalsign_right[0] and len(rule.equalsign_right) == 1):
        return 2
    else:
        return 0

# get relationship between active_edge and the chart's part
def get_rela_edge2chart(active_edge , chart , run_point):
    judge_part = chart.part
    active_edge_break_index = active_edge.break_point
    judge_edge_part =  active_edge.rule.equalsign_right[active_edge_break_index]
    judge_len = active_edge.rule.right_len
    if (active_edge.end_point == chart.begin_point):
        if (judge_edge_part == judge_part and active_edge_break_index + 1 < judge_len):
            return 1
        elif (judge_edge_part == judge_part and active_edge_break_index + 1  == judge_len):
            return 2
        else :
            return 0
    else:
        return 0


############################################################################################
# main()
############################################################################################
def main():
    # define global
    global run_point
    global active_edge_list
    global agenda
    global chart_list
    global rule_list

    # get the test sentences rule and dic
    sentences = read_sentences(sentences_file_dir)
    test_sentence = sentences[0]
    sen_len = len(test_sentence)
    dic = get_dic(dic_file_dir)
    rules = get_rules(rule_file_dir)

    # begin chart parser
    while (run_point < sen_len or bool(1 - agenda.empty())) :
        # step 1
        if agenda.empty() :
            temp_part = dic[test_sentence[run_point]]
            temp_agenda = agenda_item(temp_part , run_point , run_point + 1)
            agenda.put(temp_agenda)

        # step 2
        opera_agenda = agenda.get()

        # step 3
        for temp_rule in rules:
            flag_agenda2rules = get_rela_agenda2rules(opera_agenda , temp_rule)
            # print ('flag_agenda2rules : ' + str(flag_agenda2rules))
            if  1 == flag_agenda2rules :
                new_active_edge = active_edge(temp_rule , 1 , opera_agenda.begin_point , opera_agenda.end_point)
                active_edge_list.append(new_active_edge)
            elif 2 == flag_agenda2rules :
                new_agenda = agenda_item(temp_rule.equalsign_left , opera_agenda.begin_point , opera_agenda.end_point)
                agenda.put(new_agenda)
                print ('add agenda local 1 : ' +  new_agenda.part + ' ' + str(new_agenda.begin_point) + ' -> ' + str(new_agenda.end_point))

        # step 4
        new_chart = chart(opera_agenda.part , opera_agenda.begin_point , opera_agenda.end_point)
        chart_list.append(new_chart)

        # step 5
        for temp_active_edge in active_edge_list:
            flag_edge2chart = get_rela_edge2chart(temp_active_edge, new_chart ,run_point)
            # print ('flag_edge2chart : ' + str(flag_edge2chart))
            if 1 == flag_edge2chart :
                temp_active_edge.break_point = temp_active_edge.end_point + 1
                temp_active_edge.end_point = new_chart.end_point
            elif 2 == flag_edge2chart :
                useful_part = temp_active_edge.rule.equalsign_left
                new_agenda = agenda_item(useful_part,temp_active_edge.begin_point,new_chart.end_point)
                # active_edge_list.remove(temp_active_edge)
                agenda.put(new_agenda)
                print ('add agenda local 2 : ' +  new_agenda.part + ' ' + str(new_agenda.begin_point) + ' -> ' + str(new_agenda.end_point))
                # test
                '''
                print ('add new agenda : ')
                print (new_agenda.part + ' : ', end='')
                print (str(new_agenda.begin_point) + ' -> ' + str(new_agenda.end_point))
                '''

        # test
        print(run_point)
        print ('chart : ')
        for item in chart_list:
            print (item.part + ' : ', end='')
            print (str(item.begin_point) + ' -> ' + str(item.end_point))
        print ('active_edge : ')
        for item in active_edge_list:
            print (item.rule.equalsign_left + ' -> ', end='')
            print (item.rule.equalsign_right , end='')
            print ('|' , end = '')
            print (str(item.begin_point) + ' -> ' + str(item.end_point) + ' | ' + str(item.break_point))
        print('==========================================================')
        # end

        run_point = new_chart.end_point

    print ("finish ! ")


if __name__ == '__main__':
    main()
