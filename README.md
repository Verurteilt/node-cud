#Django and Node.js

Custom Users with Django 1.5 and realtime with node.js an socket-io

#Dependencies
	Django 1.5
	Tweepy (pip install tweepy)
	Nodejs
	Npm
	Socket.io
Step 1 go to settings.py and comment `nodejs` app and comment `AUTH_USER_MODEL` variable

then sync the db

`python manage.py syncdb`

When python ask you `Do you want to create a super user` write no

then after this go to settings.py and uncomment `nodejs` app and `AUTH_USER_MODEL` variable

and migrate `python manage.py migrate nodejs` and then create a superuser `python manage.py createsuperuser`

then install `socket.io` with `npm install scoket.io` and run the nodejs server and the django server

`node app.js` into nodejs folder and `python manage.py runserver`

Then go to `localhost:8000/login` write your email and password. Go to myprofile in the menu and click Edit Profile after this add a consumer key a consumer secret key a token and a access token secret, you can obtain them in

(http://dev.twitter.com/apps/new) Be sure give the permissions `Read and write`

After you add keys and token now you can tweet, go to `localhost:8000/tweet` and in other tab or other browser
open at the same time `localhost:8000` and tweet something and you will se the realtime in `localhost:8000`