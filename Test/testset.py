x = set('runoob')
y = set('google')
print(x)
print(y)
print(x & y)
print(x | y)
print(x - y)
print(y - x)
print(y ^ x)
print(x ^ y)


ttt = ['Jessie', 'Feyman', 37, 7]
details = set(ttt)
print(details)

test_set1 = {'name', 'age', 'birthday'}
test_set1.add('sex')
print(test_set1)
#{'name', 'birthday', 'sex', 'age'}

final_set = {"set"}
add_set = {"add_set1", "add_set2"}
add_list = ["add_list1", "add_list2"]
add_tuple = ("add_tuple1", "add_tuple2")
add_string = "add_string"
final_set.update(add_set)
final_set.update(add_list)
final_set.update(add_tuple)
final_set.update(add_string)
print(final_set)
# {'s', 'r', 'add_list1', 'add_tuple2', 'set', 'g', 't', 'i', 'a', 'n', 'add_set1', 'd', '_', 'add_tuple1', 'add_list2', 'add_set2'}

for i in final_set:
    print(i)

names_set_01 = {'Neo', 'Lily', 'Jack', 'Adem'}
names_set_02 = {'Jack', 'Adem', 'Albina'}
names_isdisjoint = names_set_01.isdisjoint(names_set_02)
print(names_isdisjoint) # >>> False

names_set_01 = {'Neo', 'Lily', 'Jack'}
names_set_02 = {'Ben', 'Adem', 'Albina'}
names_isdisjoint = names_set_01.isdisjoint(names_set_02)
print(names_isdisjoint) # >>> True