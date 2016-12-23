import flickrapi
import urllib
import json
import random
import filecmp
import shutil
import os.path
from pprint import pprint
import numpy as np
import cv2

api_key = u'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
api_secret = u'xxxxxxxxxxxxxxxxxxxx'
access_token = u'xxxxxxxxxxxxxxxxxx-xxxxxxxxxxxx'
token_secret = u'xxxxxxxxxxxxx'

user_id = "xxxxxxxxxxx"

flickr = flickrapi.FlickrAPI(api_key, api_secret,format='parsed-json')

photos = []

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='read'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=u'read')
    print(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = unicode(raw_input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

print('Step 2: use Flickr')
resp = flickr.people.getPhotos(api_key=api_key,user_id=user_id, per_page='500',authenticated=True, page=1,extras="url_z");

data_filename = 'public/data.json'

# get and save the data

count = 0

p = resp['photos']['photo']

# keep the most recent two
p0 = resp['photos']['photo'][0]
p1 = resp['photos']['photo'][1]

# shuffle the rest
random.shuffle(p)
p.insert(0, p1)
p.insert(0, p0)

for pp in p:

# copy??
    photo = pp
    #print photo

    if(count < 20):

# check if we have the image

      pic_id = photo['id']+'_'+photo['secret']+'_b.jpg'
      photo['file_name'] = "images/"+pic_id

      url_b = 'https://farm'+str(photo['farm'])+'.staticflickr.com/'+photo['server']+'/'+pic_id
      print("looking at url_b ",url_b)

      img_f_name = 'public/images/'+pic_id

      if(os.path.isfile(img_f_name)):
        print "got the file, not downloading"

      else:

# if we don't, write to file
        img = urllib.urlopen(url_b)

        print("writing "+img_f_name)

        with open(img_f_name, 'w') as f:
          f.write(img.read())

# do face detection
      print "loading and face detecting on "+img_f_name

      gray = cv2.imread(img_f_name,cv2.CV_LOAD_IMAGE_GRAYSCALE)
      faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  
      faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
      )

      print "Found {0} faces!".format(len(faces))
      height, width = gray.shape 
      print str(width)
      print str(height)

      photo['width'] = str(width)
      photo['height'] = str(height)

    # opencv is in pixels, starts top left
    # I think we're lookign for hightest value of y?
      highest_face_y = ''
      highest_face_x = ''
      for (x, y, w, h) in faces:
        ##cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print('highest_face is currently ',highest_face_y)
        print('y is currently ',y)
        if(highest_face_y == "" or (int(y) < int(highest_face_y))):
          highest_face_y = y
          highest_face_x = x
          print('setting highest_face ',highest_face_y)

      print('final highest_face ',highest_face_y)
  
      if(highest_face_y!=''):
        ##cv2.rectangle(img, (0, 0), (highest_face_x, highest_face_y), (255, 255, 0), 2)
        hf_int = int(highest_face_y) #I'm baffled
        photo['highest_face'] = str(hf_int)
      else:
        photo['highest_face'] = ''

      photo['highest_face'] = str(highest_face_y)

# end face detection

      photos.append(photo)
      count=count+1

# save the metadata

with open(data_filename, 'w') as outfile:
    zz = {}
    zz["photo"] = photos
    print "saving as "+data_filename
    json.dump(zz, outfile)
