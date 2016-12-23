import flickrapi
import urllib
import json
import random
import filecmp
import shutil
import os.path
from pprint import pprint

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

      photos.append(photo)
      count=count+1

# save the metadata

with open(data_filename, 'w') as outfile:
    zz = {}
    zz["photo"] = photos
    print "saving as "+data_filename
    json.dump(zz, outfile)
