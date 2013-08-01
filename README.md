## Prerequisites

+ **Python** 2.7.3
+ **[virtualenv](http://www.virtualenv.org/en/latest/)** 1.7.1.2 -
    Install it with pip or from distribution packages.
```bash
sudo pip install virtualenv
```
+ **PostgreSQL** 9.1.9
+ Apache **httpd** 2.2.22

## Database

1. Login to `psql`
```bash
su postgres -c psql
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
virtualenv /opt/venv/uploader
```
2. Activate created `VirtualEnv` (you have to do that for each terminal window you are going to use any Python commands)
```bash
source /opt/venv/uploader/bin/activate
```

## Web Application

0. For convenience export the application directory as an environmental variable:
```bash
export APP_DIR=/var/www/t1student0.esc.rl.ac.uk
```
1. Get the application. The app can be placed anywhere but we will use `/var/www/t1student0.esc.rl.ac.uk`.
    + unpack the `uploader.tar.gz`:
```bash
mkdir $APP_DIR
tar xvf uploader.tar.gz --strip-components 1 -C $APP_DIR
```
    + or clone it with `git`:
```bash
git clone ssh://git@bitbucket.org:mmk/stfc-uploader.git $APP_DIR
```
3. Install application dependencies using `pip`.
    1. Make sure you activated just created `VirtualEnv`.
    2. Install dependencies using either:
        + provided bundle
```bash
pip install production.pybundle
```
        + or by downloading packages from the internet
```bash
pip install -r requirements.txt
```

## Configure the Uploader

1. Open `archer/settings/prod.py` and set the database connection credentials
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
    1. Set `PROJECT_ROOT` to application directory (`$APP_DIR`):
```python
    PROJECT_ROOT = '/var/www/t1student0.esc.rl.ac.uk/'
```
    2. Change `SECRET_KEY` (production only):
```python
    SECRET_KEY = 'apksigo!uh4gth@7nco7y2biavj=0fxd0b3@2!ax6*rb29fq=w'
```
    9. Customize if needed:
        1. modify `MEDIA_ROOT` to set location of uploaded files on the filesystem:
```python
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads/')
```
        2. modify `MEDIA_ROOT` to set url to uploaded files:
```python
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
    MEDIA_URL = 'http://t1student0.esc.rl.ac.uk/uploads/'
```
        3. modify `STATIC_ROOT` to ...
```python
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collectstatic/')
```
        4. modify `STATIC_URL` to ...
```python
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
    STATIC_URL = '/static/'
```

9. ...

## httpd

1. Make sure `mod_wsgi` is installed and enabled.
    + check if `mod_wsgi` is available:
```bash
apache2ctl -M | grep wsgi
```
    + if `mod_wsgi` is not present, install it from distribution packages
    + make sure `mod_wsgi` is enabled:
        + use `a2enmod`:
```bash
a2enmod wsgi
```
        + or if `a2enmod` is not available simply create symbolic links:
```bash
cd /etc/apache2/mods-enabled
ln -s ../mods-available/wsgi.load
ln -s ../mods-available/wsgi.conf
```

2. Copy `httpd.uploader.conf` to `sites-available` of `httpd`
```bash
cp $APP_DIR/httpd.uploader.conf /etc/apache2/sites-available/uploader.conf
```
3. Set the paths to the certificates:
    1. set host certificate
    2. set host private key
    3. set path to certificates directory
```apache
  SSLCertificateFile    /path/hostcert.pem
  SSLCertificateKeyFile /path/hostkey.pem
  SSLCACertificatePath  /path/certificates
```

4. Adjust the configuration for this site by changing the paths if you used different ones than in this guide.
    1. ...
5. Enable the site
    + use `a2ensite`:
```bash
a2ensite uploader.conf
```
    + or ir `a2ensite` is not available simply create symbolic link:
```bash
cd /etc/apache2/sites-enabled
ln -s ../sites-available/uploader.conf
```
6. Set correct `chmod`/`chown` for `media`, `uploads` and `cvmfs` directories.
...

## Uploader initial data
...

# Development

## Create a bundle

```bash
pip bundle dev.pybundle -r requirements.txt
```

## About

The application is developed by [Michał Knapik](http://github.com/mknapik) for [SCD STFC](http://www.stfc.ac.uk/SCD)

## License

???