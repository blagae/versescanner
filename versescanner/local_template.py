# copy this file to versescanner/local.py

# DO NOT CHANGE THE VARIABLE NAMES OF THE PROPERTIES

# you will only need to define this if you want to use utils.recreate_db()
DB_SUPERUSER_PASSWORD = 'mp'

# change database settings at will
# if you use something other than SQLite, you will need to
# consult the Django docs for database settings
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydb.db'
    }
}

# disable this when deploying to production
DEBUG = True

# add your name and e-mail address
# not setting this property will cause Django errors if DEBUG_SETTING is False
# https://docs.djangoproject.com/en/1.9/ref/settings/#admins
ADMINS = []
# example: [('John', 'john@example.com')]

# replace this with a longer key
# suggestion: http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'abc'

# if you want to deploy this project on a web server, then your application needs to know the domain name
# if this doesn't apply to you, then you can leave this empty, or set it to None
ALLOWED_HOSTS = []
# example: ['myaccount.example.com']

# in order to use file-based session management, we need a folder on the server that can store these files
# for inspiration, a few default locations have been provided in the .gitignore file
SESSION_FILE_PATH = "/path/to/temp_folder/"
