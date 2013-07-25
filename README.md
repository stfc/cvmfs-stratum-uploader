## Prerequisites

+ **Python** 2.7.3
+ **[virtualenv](http://www.virtualenv.org/en/latest/)** 1.7.1.2 -
    Install it with pip or from distribution packages.
```bash
$ [sudo] pip install virtualenv
```
+ **PostgreSQL** 9.1.9
+ Apache **httpd** 2.2.22

## Database

1. Login to `psql`
```bash
$ su postgres -c psql
```
2. Create a new database user `django` (you can also use an existing one).
```sql
CREATE USER django WITH PASSWORD 'password';
```
3. Create a new database `uploader` with created owner.
```sql
CREATE DATABASE uploader WITH OWNER=django;
``` 

## VirtualEnv

1. Create new `VirtualEnv` for the project. You can choose any location from which `httpd` can read from.
```bash
$ virtualenv /opt/venv/uploader
```
2. Activate created `VirtualEnv` (you have to do that for each terminal window you are going to use any Python commands)
```bash
$ source /opt/venv/uploader/bin/activate
```

## Web Application

1. Get the application. The app can be placed anywhere but we will use `/var/www/t1student0.esc.rl.ac.uk`.
    + unpack the `archer.tar.gz`:
    ```bash
# mkdir /var/www/t1student0.esc.rl.ac.uk
# tar xvf archer.tar.gz --strip-components 1 -C /var/www/t1student0.esc.rl.ac.uk
```
    + or clone it with `git`:
    ```bash
# git clone git://repository_address/archer.git /var/www/t1student0.esc.rl.ac.uk/
```
3. Install application dependencies using `pip`.
    1. Make sure you activated just created `VirtualEnv`.
    2. Install dependencies using either:
        + provided bundle
        ```bash
$ pip install production.pybundle
```
        + or by downloading packages from the internet
        ```bash
$ pip install -r requirements.txt
```

## Configure the Uploader

1. Open `archer/settings/dev.py` and set the database connection credentials
    ```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uploader',
        'USER': 'django',
        'PASSWORD': 'password',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
```
2. Open `archer/settings/common.py` and set paths to directories.
    1. Set `PROJECT_ROOT` to application directory:
    ```bash
PROJECT_ROOT = '/var/www/t1student0.esc.rl.ac.uk/'
```
    2. Change `SECRET_KEY` (production only):
    ```bash
SECRET_KEY = 'apksigo!uh4gth@7nco7y2biavj=0fxd0b3@2!ax6*rb29fq=w'
```
    9. Customize if needed:
        1. modify `MEDIA_ROOT` to set location of uploaded files on the filesystem:
        ```bash
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads/')
```
        2. modify `MEDIA_ROOT` to set url to uploaded files:
        ```bash
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://t1student0.esc.rl.ac.uk/uploads/'
```
        3. modify `STATIC_ROOT` to ...
        ```bash
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collectstatic/')
```
        4. modify `STATIC_URL` to ...
        ```bash
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'
```

9. ...

## httpd

1. Copy `archer.conf` to `sites-available` of `httpd`
```bash
# cp /var/www/t1student0.esc.rl.ac.uk/archer.conf /etc/apache2/sites-available/uploader.conf
```
2. Set the paths to the certificates:
    1. set host certificate
    2. set host private key
    3. set path to certificates directory

    ```apache
  SSLCertificateFile    /path/hostcert.pem
  SSLCertificateKeyFile /path/hostkey.pem
  SSLCACertificatePath  /path/certificates
```

3. Adjust the configuration for this site by changing the paths if you used different ones than in this guide.
    1. ...
4. Enable the site
```bash
# a2ensite uploader.conf
```

# Development

## Create a bundle

```bash
pip bundle dev.pybundle -r requirements.txt
```

## About

The application is developed by [Michał Knapik](http://github.com/mknapik) for [SCD STFC](http://www.stfc.ac.uk/SCD)

## License

???