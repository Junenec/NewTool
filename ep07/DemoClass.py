# -*- coding:utf-8 -*-
"""
Date: 2022-11-08
"""
import re
class Cat:
    """
    这是一只猫的类
    """
    def __init__(self, name):
        self.name = name
        print("我是一只猫，我的名字叫{}".format(self.name))

    def __del__(self):
        print("{}被系统回收啦".format(self.name))


if __name__ == '__main__':
    # a={1: {'id': 1, 'school': "advanced", 'name':"Jessie"},
    #    2: {'id': 2, 'school': "primary", 'name':"Tom"},
    #    3: {'id': 3, 'school': "advanced", 'name':"Cathy"},
    #    4: {'id': 4, 'school': "middle", 'name':"Jerry"},
    #    5: {'id': 5, 'school': "advanced", 'name':"Henry"}}
    #
    # for uuid in a:
    #     if a[uuid]['school'] == "primary":
    #         continue
    #     elif a[uuid]['school'] == "middle":
    #         continue
    #     else:
    #         print("name {} school {}".format(a[uuid]['name'], a[uuid]['school']))
    # thislist = ["apple", "banana", "cherry"]
    # for index in range(len(thislist)):
    #     print(index, thislist[index])

    #
    # value = 20
    # condition = 'False'
    # print(eval(condition))

    # def checkCondition(condition):
    #     symbollist = []
    #     for i in condition:
    #         if i in ['{', "("]:
    #             symbollist.append(i)
    #         elif i == "}" and len(symbollist)!=0:
    #             if symbollist[-1] == "{":
    #                 symbollist.pop()
    #             else:
    #                 return False
    #         elif i == "}" and len(symbollist)==0:
    #             return False
    #         elif i == ")" and len(symbollist)!=0:
    #             if symbollist[-1] == "(":
    #                 symbollist.pop()
    #             else:
    #                 return False
    #         elif i == ")" and len(symbollist) == 0:
    #             return False
    #         else:
    #             continue
    #     if len(symbollist) == 0:
    #         return True
    #     else:
    #         return False
    #

    # conditions = ['{a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c} == 10 and {3383c8c2-ef79-4591-a474-e1ae47642068}==0',
    #               '({a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c} == 10) or ({3383c8c2-ef79-4591-a474-e1ae47642068}==0)',
    #               'not ({a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c} < 2)',
    #               '{16bb651e-831d-4447-9237-586cf57059a4} == 1',
    #               '{16bb651e-831d-4447-9237-586cf57059a4} == 1 2']

    # conditions = ['{a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c == 10 and {3383c8c2-ef79-4591-a474-e1ae47642068}==0',
    #               '(a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c} == 10) or ({3383c8c2-ef79-4591-a474-e1ae47642068}==0)',
    #               'not ({a3cc2f37-2fdf-4f63-93e8-e51cb9d7f37c)} < 2)',
    #               '{16bb651e-831d-4447-9237-586cf57059a4) == 1',
    #               '{16bb651e-831d-4447-9237-586cf57059a4})== 1 2']
    # conditionChecking = True
    # for condition in conditions:
    #     if checkCondition(condition):
    #         start = [i.start() for i in re.finditer('{', condition)]
    #         end = [i.start() for i in re.finditer('}', condition)]
    #         for i in range(len(start)):
    #             print(condition[start[i]:end[i]+1])
    # para = {'Name': 'PP:ConditionParameter:Enum', 'type': 'Enum', 'uuid': '{16bb651e-831d-4447-9237-586cf57059a4}', 'parent': '{d5c69ae6-c133-40e2-87fa-29b8cca114e1}', 'Description': '', 'Notes': '', 'Label_en': 'Enum', 'Label_de': 'Enum', 'DefaultKeysArr': [1], 'EnumeratorArr': [[1, '', '', ''], [2, '', '', ''], [3, '', '', '']], 'currentValue': None}
    # print(para['Name'].count(":"))
    # para['Name'].replace(":","_")
    # print(type(para['Name']))
    # print(para['Name'])
    #
    # test = "PP:ConditionParameter:Enum"
    # print(type(test))
    # test.replace("P", "d")
    # print(test.replace("P", "d"))



    # pplist = {'{a5640904-18c7-4505-93b3-e2043c03dc17}': {'Name': 'PP_DeviceStatus_Testing_Completed', 'type': 'Enum', 'uuid': '{a5640904-18c7-4505-93b3-e2043c03dc17}', 'parent': '{bda06cbe-6992-435c-b95d-48cb939daa7a}', 'Description': '', 'Notes': '', 'Label_en': 'Testing Completed', 'Label_de': 'Testing Completed', 'DefaultKeysArr': [1], 'EnumeratorArr': [[1, 'No', 'No', 'No'], [2, 'Yes', 'Yes', 'Yes']], 'currentValue': 10},
    #           '{06983fac-73b2-4022-bc96-3c56972cabde}': {'Name': 'PP_DeviceStatus_Testing_Result', 'type': 'Integer', 'uuid': '{06983fac-73b2-4022-bc96-3c56972cabde}', 'parent': '{bda06cbe-6992-435c-b95d-48cb939daa7a}', 'Description': '', 'Notes': '', 'Label_en': 'Testing Result', 'Label_de': 'Testing Result', 'Unit': 'mg/L', 'Default': 0, 'Minimum': 0, 'IsMinNegInfinite': True, 'Maximum': 0, 'IsMaxInfinite': True, 'currentValue': 0, 'Source': ['Web UI:\\Operation\\Start Testing', 'Device UI:\\Operation\\Testing Result\\Testing Result']}
    #           }
    # conditions = ['{a5640904-18c7-4505-93b3-e2043c03dc17} == 10 and {06983fac-73b2-4022-bc96-3c56972cabde}==0']
    # for condition in conditions:
    #     start_index = [i.start() for i in re.finditer('{', condition)]
    #     end_index = [i.start() for i in re.finditer('}', condition)]
    #     print(start_index,end_index)
    #     ppuuidlist = []
    #     for i in range(len(start_index)):
    #         print(condition[start_index[i]:end_index[i] + 1])
    #         ppuuidlist.append(condition[start_index[i]:end_index[i] + 1])
    #     for ppuuid in ppuuidlist:
    #         ppname = pplist[ppuuid]['Name']
    #         locals()[ppname] = pplist[ppuuid]['currentValue']
    #         condition = condition.replace(ppuuid, ppname)
    #     print(condition)
    #     print(eval(condition))
    #
    # result = eval("1 + 1")
    # print(result)
    # result = eval("'A+' * 5")
    # print(result)  # A+A+A+A+A+
    #
    # result = eval("[1, 2, 3, 4]")
    # print(result)  # [1, 2, 3, 4]
    # print(type(result)) # <class 'list'>
    #
    # result = eval("{'name': '小夏', 'age': 30}")
    # print(result)  # {'name': '小夏', 'age': 30}
    # print(type(result)) # <class 'dict'>
    #
    # name = "Jessie"
    # result1 = eval("name == 'Jessie'")
    # result2 = eval("name != 'Jessie'")
    # print(result1) # True
    # print(not result2) # False
    # def xx():
    #     test1 = [11, 12, 13]
    #     test2 = [21, 22, 23]
    #     for i in test1:
    #        print(i)
    #        for j in test2:
    #            if j==22:
    #                return
    #            else:
    #                print(j)
    #
    # xx()

    p1 = [1]
    p2 = [1,2,3]
    p3 = []
    str = str(p2[0])+' '+str(p2[1])
    print(str)

    # tee = [
    #     {
    #         "Name": "PP:HmiBlockSpecific:ShowSubpage",
    #         "type": "Enum",
    #         "uuid": "{3f359f9f-2b19-4aa1-83f1-e593e1448a7d}",
    #         "parent": "{86a23c02-a713-4456-8a36-84522510fd82}",
    #         "Description": "",
    #         "Notes": "",
    #         "Label_en": "Show subpage",
    #         "Label_de": "Zeige Unterseite",
    #         "DefaultKeysArr": [0],
    #         "EnumeratorArr": [
    #             [0, "False", "False", "False"],
    #             [1, "True", "True", "True"]
    #         ]
    #     },
    #     {
    #         "Name": "PP:HmiBlockSpecific:NextPage",
    #         "type": "Enum",
    #         "uuid": "{0f86e716-42e5-49ec-bcbf-88300d675ff9}",
    #         "parent": "{86a23c02-a713-4456-8a36-84522510fd82}",
    #         "Description": "",
    #         "Notes": "",
    #         "Label_en": "Process finished",
    #         "Label_de": "Prozess abgeschlossen",
    #         "DefaultKeysArr": [
    #
    #         ],
    #         "EnumeratorArr": [
    #             [
    #                 0,
    #                 "Please select!",
    #                 "Please select!",
    #                 "Bitte auswählen!"
    #             ],
    #             [
    #                 1,
    #                 "Finished!",
    #                 "Finished!",
    #                 "Fertig!"
    #             ]
    #         ]
    #     }
    # ]
    # for t in tee:
    #     print(t['DefaultKeysArr'])
    #     print(len(t['DefaultKeysArr']))
    #

    aa = {'System': [], "Web UI": [], "Device UI": []}
    aa['System'].append()
