# import os
# 

path = '256_ObjectCategories'

# categories = []
# for root, dirs, files in os.walk(path, topdown=False):
#     for name in dirs:
#         categories.append(name.split('.')[-1])
# 
# 
# print("Your list is: ", categories)
# 
# name = input("Pick category: ")
# 
# if any(name in s for s in categories):
#     print(list(filter(lambda x: name in x, categories)))
# else:
#     print("No category of {0}".format(name))
# 
# 
# 
# 
import os, random
n=0
random.seed();
for root, dirs, files in os.walk(path):
  for name in files:
    n=n+1
    if random.uniform(0, n) < 1: rfile=os.path.join(root, name)
print(rfile)
