# gitlab-redmine-1clk-deleter
Delete Gitlab and Redmine account in one click.  

# Install:  

$ git clone git@github.com:murielll/gitlab-redmine-1clk-deleter.git  
$ cd gitlab-redmine-1clk-deleter  
$ sudo apt-get install python-virtualenv  
$ virtualenv py2  
$ ./py2/bin/activate  
$ pip install -r requirements.txt  

Sync database:  
$ ./manage.py migrate  

Create admin:  
$ ./manage.py createsuperuser  

Admin URL: http://your.domain/admin

# Test run:  
$ ./manage.py runserver  

# UWSGI run:
In deploy/ directory stored templates for nginx and uwsgi. Change them to suit your environment or use another.

$ sudo pip install uwsgi  

Change deploy/uwsgi.ini for your project.  

Start:   
$ uwsgi --ini deploy/uwsgi.ini  
Stop:    
$ uwsgi --stop /tmp/uwsgi-$USER.pid   
