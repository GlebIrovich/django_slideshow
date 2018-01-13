import pandas as pd
import os
from django.conf import settings
#from boto.s3.connection import S3Connection


import zipfile
import random, string



def randomword(length):
   letters = string.ascii_letters
   name = ''.join(random.choice(letters) for i in range(length))
   name = name.lower()
   return name

# extract the archive
def unzip(source_path, output_path): # ADD OUTPUT ? , output_path

    archive = zipfile.ZipFile(source_path)
    # set path
    archive.extractall(output_path)
    try:
        os.remove(source_path)
    except OSError:
        pass
    




def generate_json(path, class_name):
    path = settings.MEDIA_ROOT + path
    folders = os.listdir(path)
    folders = [x for x in folders if x[0]!='.']
    folders.sort()
    dic = {}
    
    # change this line to the actual class name
    dic['class_title'] = class_name
    i = 0 
    dic['lectures'] = {}
    for folder in folders:
        
        subpath = path + '/' + folder + '/'
        # check if there is at least one JPEG in the directory
        if len([check for check in os.listdir(subpath) if (check[-3:] == 'jpg') or (check[-4:] == 'jpeg') or (check[-3:] == 'png')]) != 0:
        
            i+=1
            
            subpath_to_csv = path + '/' + folder + '/' + 'details.csv'
            
            data = pd.read_csv(subpath_to_csv, header = None)
            
            dic['lectures']['lecture{}'.format(i)]={'lecture_title':data.iloc[0][1]}
            if len(data) > 1:
                for n in list(range(1,len(data))):
                    dic['lectures']['lecture{}'.format(i)]['subchapters']={}
                for n in list(range(1,len(data))):   
                    dic['lectures']['lecture{}'.format(i)]['subchapters']['sub{}'.format(n)]={}
                    dic['lectures']['lecture{}'.format(i)]['subchapters']['sub{}'.format(n)]['title'] = data.iloc[n][0]
                    dic['lectures']['lecture{}'.format(i)]['subchapters']['sub{}'.format(n)]['slide'] = data.iloc[n][1]
            
            # add inforamtion about slides' paths
            slides = os.listdir(subpath)
            slides = [file for file in slides if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")]
            slides.sort()
            dic['lectures']['lecture{}'.format(i)]['slides']={}

            # Change subpath so that media correctly displayed
            
            media_link = '/media/' + '/'.join(subpath.split('/')[-4:])

            for slide in slides:
                dic['lectures']['lecture{}'.format(i)]['slides'][slide]=media_link + slide
    
    #encode=json.dumps(dic)   
    return dic

