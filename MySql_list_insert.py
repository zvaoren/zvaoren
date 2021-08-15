
list = []
list.append("element1")
list.append("element2")
list1 = list.copy()
print(list1)
list1.append(list[1])
print(list1)

quit()


L1 = ['hel-lo', 'world', 'bye', 'python']
values = [[item] for item in L1]
cursor.executemany(u"INSERT INTO `instability`(`ap_name`) VALUES (%s)", values)

query = "INSERT INTO round1 (details) VALUES (%s)"
c = conn.cursor()
c.executemany(query, [(r,) for r in results])

data = "INSERT INTO ... VALUES ... %s ..."
cursor.execute(data, (data_input,))
#quora says (%s) is a security issue...?
