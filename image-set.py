import os


categories = []
for root, dirs, files in os.walk('256_ObjectCategories', topdown=False):
    for name in dirs:
        categories.append(name.split('.'))


print("Your list is: ", categories)

name = input("Pick category: ")

if any(name in s for s in categories):
    print(list(filter(lambda x: name in x, categories)))
else:
    print("No category of {0}".format(name))


