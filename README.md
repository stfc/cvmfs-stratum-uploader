# CVMFS Stratum-0 Uploader

[![Build Status](https://travis-ci.org/stfc/cvmfs-stratum-uploader.png)](https://travis-ci.org/stfc/cvmfs-stratum-uploader)

Provides interface for uploading and distributing software through cvmfs repositories.

Uses Certificate Authentication provided by Apache `httpd` web server (or others).

## Installation

For production best way to deploy the application is to install it with RPMs. See how to [build RPMs](#building-rpms).

1. Install all dependencies:
    1. `httpd`
    2. `python`
    3. `mod_wsgi` for **httpd**
    4. Python packages:

        ```bash
        rpm -i Django-*.*.*-*.noarch.rpm \
            South-*.*.*-*.noarch.rpm \
            django-guardian-*.*.*-*.noarch.rpm \
            django-bootstrap-toolkit-*.*.*-*.noarch.rpm
        ```
2. Install **uploader** and **config**:

    ```bash
    rpm -i cvmfs-stratum-uploader-config-*.*.*-*.noarch.rpm cvmfs-stratum-uploader-*.*.*-*.noarch.rpm
    ```
3. Provide `ALLOWED_HOSTS` list in `/var/www/cvmfs-stratum-uploader/application.cfg`.
For development can be set to `ALLOWED_HOSTS: *`.
4. Restart `httpd`
5. Open https://hostname/setup and setup an admin account:
    1. Provide `DN` of the application's admin
    2. Log in as admin and setup the application

## Building RPMs

### Prerequisites

+ **Python** `2.6.6`
+ **Sqlite3** `3.6.20`
+ Apache **httpd** `2.2.22`
+ Git and Mercurial (in case of downloading sources from repositories)

### Dependencies

1. Download all dependencies:
    + [Django](https://www.djangoproject.com/)`>=1.5.1`
    + [South](http://south.aeracode.org/)`>=0.8.1`
    + [django-guardian](http://pythonhosted.org/django-guardian/)`>=1.1.1`
    + [django-bootstrap-toolkit (fork: `stfc`)](http://github.com/stfc/django-bootstrap-toolkit)

2. Current versions can be downloaded as follows:
    + download `tar`/`zip`s from project websites and unpack
    + or fetch sources from repositories and switch to correct branch/tag:

        ```bash
        git clone https://github.com/django/django.git
        hg clone https://bitbucket.org/andrewgodwin/south
        git clone https://github.com/lukaszb/django-guardian.git
        git clone https://github.com/stfc/django-bootstrap-toolkit.git

        ```

        ```bash
        cd ./django; git checkout 1.5.1
        cd ../south; hg checkout 0.8.2
        cd ../django-guardian; git checkout v1.1.1
        cd ../django-bootstrap-toolkit; git checkout master
        cd ../

        ```

3. Build RPM for all dependencies with setuptools:

    ```bash
    cd ./django
    python setup.py bdist_rpm --requires='python'
    cd ../south
    python setup.py bdist_rpm --requires='python >= 2.6, Django >= 1.2'
    cd ../django-guardian
    python setup.py bdist_rpm
    cd ../django-bootstrap-toolkit
    python setup.py bdist_rpm --requires='Django >= 1.5'
    cd ../
    
    cp */dist/*noarch.rpm .
    ```

### cvmfs-stratum-uploader

1. Fetch newest version of `cvmfs-stratum-uploader`:

    ```bash
    git clone https://github.com/stfc/cvmfs-stratum-uploader.git
    ```

2. Build RPM with setuptools:

    ```bash
    cd cvmfs-stratum-uploader
    python setup.py bdist_rpm
    cd ../
    cp cvmfs-stratum-uploader/dist/*.noarch.rpm .
    ```

### Cut-Across

The commands below should download the application and all dependencies and create required RPMs.


    mkdir cvmfs-stratum-uploader-rpms
    cd cvmfs-stratum-uploader-rpms

    git clone https://github.com/django/django.git
    hg clone https://bitbucket.org/andrewgodwin/south
    git clone https://github.com/lukaszb/django-guardian.git
    git clone https://github.com/stfc/django-bootstrap-toolkit.git
    git clone https://github.com/stfc/cvmfs-stratum-uploader.git

    cd ./django
    git checkout 1.5.1
    python setup.py bdist_rpm --requires='python'
    cd ../south
    hg checkout 0.8.2
    python setup.py bdist_rpm --requires='python >= 2.6, Django >= 1.2'
    cd ../django-guardian
    git checkout v1.1.1
    python setup.py bdist_rpm
    cd ../django-bootstrap-toolkit
    git checkout master
    python setup.py bdist_rpm --requires='Django >= 1.5'
    cd ../cvmfs-stratum-uploader 
    git checkout master
    python setup.py bdist_rpm
    cd ../

    cp */dist/*noarch.rpm .

### cvmfs-stratum-uploader-config

Go to [cvmfs-stratum-uploader-config](https://github.com/stfc/cvmfs-stratum-uploader-config) project
for detailed description about building RPM with configuration.

## Development

### Prerequisites

+ **Python** `2.6.6`
+ **Sqlite3** `3.6.20`
+ Apache **httpd** `2.2.22`
+ Git and Mercurial
+ **[virtualenv](http://www.virtualenv.org/en/latest/)** `1.7.1.2` - Install it with pip or from distribution packages.

    ```bash
    sudo pip install virtualenv
    ```
+ **virtualenvwrapper** `4.1.1`

    ```bash
    sudo pip install virtualenvwrapper
    source /usr/local/bin/virtualenvwrapper.sh
    ```
+ For convenience export the application directory as an environmental variable:

```bash
export APP_DIR=/var/www/cvmfs-stratum-uploader
```

### Database

#### sqlite3

1. Create empty database file with proper `chmod`:

    ```bash
    touch $APP_DIR/db/uploader.sqlite3
    chmod 600 $APP_DIR/db/uploader.sqlite3
    ```
2. Set `db` directory security:
    ```bash
    chmod 770 $APP_DIR/db
    chgrp www-data $APP_DIR/db
    ```

#### other

Application should work with any database supported by Django but only **Sqlite3** is supported by the project.

### VirtualEnv

1. Create new `VirtualEnv` for the project. You can choose any location from which `httpd` can read from.

    ```bash
    virtualenv /opt/venv/uploader
    ```
2. Activate created `VirtualEnv` (you have to do that for each terminal window you are going to use any Python commands)

    ```bash
    source /opt/venv/uploader/bin/activate
    ```

### Web Application

1. Get the application. The app can be placed anywhere but we will use `/var/www/cvmfs-stratum-uploader`.
    + unpack the `uploader.tar.gz`:

        ```bash
        mkdir $APP_DIR
        tar xvf uploader.tar.gz --strip-components 1 -C $APP_DIR
        ```
    + or clone it with `git`:

        ```bash
        git clone https://github.com/stfc/cvmfs-stratum-uploader.git $APP_DIR
        ```

3. Install application dependencies using `pip`.
    1. Make sure you activated just created `VirtualEnv`.
    2. Install dependencies with pip:

            ```bash
            pip install -r requirements.txt
            ```

### Configure the Uploader

1. Open `uploader/settings/production.py` and set the database connection credentials

    ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '%s/db/uploader.sqlite3' % PROJECT_ROOT,
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            },
        }
    ```

2. Open `uploader/settings/common.py` and set paths to directories.
    2. Change `SECRET_KEY` (production only):

        ```python
            SECRET_KEY = 'apksigo!uh4gth@7nco7y2biavj=0fxd0b3@2!ax6*rb29fq=w'
        ```
    9. Customize if needed:
        1. Set `PROJECT_ROOT` to application directory (`$APP_DIR`):

            ```python
                PROJECT_ROOT = '/var/www/cvmfs-stratum-uploader/'
            ```
        1. Set `HOSTNAME`:
            
            ```python
            HOSTNAME = get_host_name()
            ```
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
                MEDIA_URL = 'http://__FULL_HOST_NAME__/uploads/'
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

### httpd

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

2. Link `httpd.uploader.conf` to `sites-available` of `httpd`

    ```bash
    ln -s $APP_DIR/httpd.uploader.conf /etc/apache2/sites-available/uploader.conf
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
3. Set the correct `WSGIPythonPath`. It should look like `$APP_DIR:$VENV_DIR/lib/$PYTHON_VERSION/site-package`.
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


### Uploader initial schema and data

1. The database can be initialized with `manage-cvmfs-stratum-uploader.py`:
    1. Create database structure:
        
        ```bash
        DJANGO_CONFIGURATION=production python manage-cvmfs-stratum-uploader.py syncdb
        DJANGO_CONFIGURATION=production python manage-cvmfs-stratum-uploader.py migrate
        DJANGO_CONFIGURATION=production python manage-cvmfs-stratum-uploader.py init_flatpages
        ```

### Asset pipeline

Project is using [guard](https://github.com/guard/guard) to compile and minify static assets like CSS and JS.
Application is using Coffescript and SASS.

To run `guard` Ruby and Bundler is required. To install dependencies run:
```bash
bundle
```

All Ruby gems should be installed. To monitor changes and compile assets automatically run `guard`:
```bash
guard
```

# About

The application was developed by [Michał Knapik](http://github.com/mknapik) for [SCD STFC](http://www.stfc.ac.uk/SCD)

# License

    Copyright 2013 Science and Technology Facilities Council UK

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
