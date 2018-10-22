<img src="https://raw.githubusercontent.com/cornell-dti/events-manager-android/master/cue_text_red.png" width="80" height="35"> (Cornell University Events) Backend + Website v1.0
======
Backend: A system that supports APIs to access data about Events and Organizations etc. on Cornell's Ithaca campus. 

Website: A **web** app for student organizations to add events for cue. Here is a list of related repositories: 
- [events manager android](https://github.com/cornell-dti/events-manager-android)
- [events manager ios](https://github.com/cornell-dti/events-manager-ios)

#### Contents
  - [About](#about)
  - [Getting Started](#getting-started)
  - [Dependencies & Libraries](#dependencies--libraries)
  - [External Documentation](#external-documentation)
  - [Screenshots](#screenshots)
  - [Contributors](#contributors)

## Getting Started
You will need **Python 3.6** to run the latest version of this app, which uses Django 2.0.1. Django can be installed using python's inbuilt _pip_ function. 

You will need IntelliJ IDEA v2018.2.5 to run the latest version of this app, which uses the following:
- React.js v.16.4.2
- Material-UI v.3.0.1.

### Setup
Run (if typing `python` gives you version 3.x):
`pip install -r requirements.txt`

Otherwise, assuming you have python3 installed, run:
`pip3 install -r requirements.txt`

Run after copying settings (See [step 1](#everyday))
`python manage.py makemigrations`

or
`python3 manage.py makemigrations`

### Everyday
Before you run anything, do this right after `git pull`:
1. Run `npm i` in the project directory to install any additional front-end frameworks.
3. Run `npm run start` or `npm run start3`, depending on whether python3 is the default version or not. This will copy `dev_settings.py` over to `settings.py` in `events_backend`, then start Webpack to hot-reload front-end changes as well as starting the Django server to hot-reload back-end changes. Isn't this an amazing script? (You can find it in `package.json`). Thank David later.

The front-end website will be located at `127.0.0.1:8000`.

## Dependencies & Libraries
 * **[Django Rest Framework](http://www.django-rest-framework.org/) v. 3.8.2** - A Django library that provides powerful authentication protocols.
 * **[Django Simple History](https://django-simple-history.readthedocs.io/en/latest/) v. 2.0** - A Django library that provides methods to store changes to models, and thus, is used to create app-specific event, org. feeds.
  * [react-avatar-editor](https://www.npmjs.com/package/react-avatar-editor) - Similar to Facebook profile picture. Allows you to crop, resize, and rotate an uploaded image. Use for event image upload in event creation.


## API Documentation
* [Backend API Documentation](https://cuevents.docs.apiary.io/) - An external Apiary documenting the endpoints for our application.



## Contributors
**2018**
* **Arnav Ghosh** - Back-End Developer
* **Jessica Zhao** - Back-End Developer
* **Jill Wu** - Back-End Developer
* **Adit Gupta** - Back-End Developer
* **David Chu** - Front-End Developer
* **Stacy Wei** - Front-End Developer

We are a part of the O-Week/Events team within **Cornell Design & Tech Initiative**. For more information, see our website [here](https://cornelldti.org/).
<img src="https://raw.githubusercontent.com/cornell-dti/design/master/Branding/Wordmark/Dark%20Text/Transparent/Wordmark-Dark%20Text-Transparent%403x.png">

_Last updated **10/21/2018**_.
