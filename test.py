import magic

path = "/Users/kylerood/Generic-Web-Classifier/256_ObjectCategories/258.elephant/258.0289.jpg"

if magic.from_file(path, mime=True) == 'image/jpeg':
        #line_px_count.append(mapcount(path))
        print("YES")

else:
    print('No')
