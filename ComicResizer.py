import zipfile
import os
#import Image

print("Working...")

path_to_zip_file = 'C:\\Users\\Eduard\\Desktop\\AAA.zip'


#Prepare temp folder name (it's just the filepath with the extension removed)
directory_to_extract_to = (os.path.splitext(path_to_zip_file)[0])


#Extract
zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
zip_ref.extractall(directory_to_extract_to)
zip_ref.close()




#Resize
"""
basewidth = 1280
img = Image.open('somepic.jpg')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save('sompic.jpg') 
"""









#Change format if necessary

#Compress

#Delete temp directory

#Rename/delete original file

#Rename new file with original filename