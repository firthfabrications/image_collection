import flickrapi
import xml.etree.ElementTree as ET
import urllib.request
import os

# Will need to go into ...\site-packages\flickrapi\core.py
# and change line 690 to photoset = list(rsp)[0]



# open the .txt list of bird species and read them in as a list 
with open("..\\bird_feeder_classifier\\texas_birds.txt") as birds_file:
    birds = [line.strip() for line in birds_file]

#get an api key and secret from flickr
api_key = u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
api_secret = u'xxxxxxxxxxxxxxxxxx'
flickr = flickrapi.FlickrAPI(api_key, api_secret)

for bird in birds:
    photos = flickr.walk(text=bird,
                        tag_mode='all',
                        tags=bird,
                        extras='url_c',
                        privacy_filters = 1,
                        per_page=500,         
                        sort='relevance')

    for i, photo in enumerate(photos):
        url = photo.get('url_c')
        #if an error occurs just keep moving
        try:
            # first 10 images are for test
            if i <= 9:
                TestDirectory = f'BIRDS/test/{bird}'
                #check if directory exists
                if not os.path.exists(TestDirectory):
                    os.makedirs(TestDirectory)
                #create file path
                filepath = os.path.join(TestDirectory, f'{i+1}.jpg')
                # Download image from the url and save it to '00001.jpg'
                urllib.request.urlretrieve(url, filepath)

            #next five images are for validation after model has been created
            elif i < 15 and i > 9:
                #create a validation folder in another location
                ValidateDirectory = f'Bird_Validate/validate/{bird}'
                #check if directory exists
                if not os.path.exists(ValidateDirectory):
                    os.makedirs(ValidateDirectory)
                #create file path
                filepath = os.path.join(ValidateDirectory, f'{i+1}.jpg')
                # Download image from the url and save it to '00001.jpg'
                urllib.request.urlretrieve(url, filepath)

            #stop after 200 total images
            elif i > 200:
                break

            #all remaining images go to training
            else:
                TrainDirectory = f'BIRDS/train/{bird}'
                #check if directory exists
                if not os.path.exists(TrainDirectory):
                    os.makedirs(TrainDirectory)
                #create file path    
                filepath = os.path.join(TrainDirectory, f'{i-9}.jpg')
                # Download image from the url and save it to '00001.jpg'
                urllib.request.urlretrieve(url, filepath)
        except:
            pass
