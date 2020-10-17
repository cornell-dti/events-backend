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
#### Installing requirements
If typing `python` gives you version 3.x):
- `pip install -r requirements.txt`

Otherwise:
- `pip3 install -r requirements.txt`

#### Copy settings from dev-settings
Linux/Mac:
- `npm run copy-settings`

Windows:
- `npm run copy-settings-windows`

#### Make migrations
If typing `python` gives you version 3.x):
- `python manage.py makemigrations`
- `python manage.py migrate`

Otherwise:
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

### Everyday
Before you run anything, do this right after `git pull`:
1. Run `npm i` in the project directory to install any additional front-end frameworks.
2. Run depending on platform:
    - Linux/Mac, python 3 is default: `npm run start`
    - Linux/Mac, python 2 is default: `npm run start3`
    - Windows, python 3 is default: `npm run start-windows`
    - Windows, python 2 is default: `npm run start3-windows`

    This will copy `dev_settings.py` over to `settings.py` in `events_backend`, then start Webpack to hot-reload front-end changes as well as starting the Django server to hot-reload back-end changes. Isn't this an amazing script? (You can find it in `package.json`). Thank David later.

The front-end website will be located at `127.0.0.1:8000`.

### Code Review
After pushing any changes to the codebase, let's get your code reviewed. Some general guidelines:
- Before you start changing any code, make sure you're synced with the master branch.
- Create a new branch off master, and give it an informative name.
- Commit your changes to this feature branch. Commit often so that you don't accidentally lose your progress!
- Open a pull request (PR), give it a meaningful title and describe the changes that you made. Take note of any future improvements or any existing bugs with the changes you made. Give some steps as to how to test the changes you've made.
- Notify others of the PR you created, and ask the relevant people to review it for you. They may leave comments and request changes, in which case you should make changes and push new commits to the same branch; the PR will update automatically!
- Finally, when the change is approved by the reviewer, you can go ahead and merge the branch into the master branch.

Some things to watch out for when reviewing someone else's code:
- Is the code documented? Are there comments that give details about what the code is doing?
- Have commented-out lines of code been deleted?
- Are your variable names clear, short, and meaningful?
- Are your functions short and have a single purpose?
- Are there redundancies in your code?

### Database
If at any point, your database becomes corrupted or you no longer have `db.sqlite3` in the directory:
1. [Copy settings](#copy-settings-from-dev-settings)
2. [Make migrations](#make-migrations)

## Dependencies & Libraries
 * **[Django Rest Framework](http://www.django-rest-framework.org/) v. 3.8.2** - A Django library that provides powerful authentication protocols.
 * **[Django Simple History](https://django-simple-history.readthedocs.io/en/latest/) v. 2.0** - A Django library that provides methods to store changes to models, and thus, is used to create app-specific event, org. feeds.
  * [react-avatar-editor](https://www.npmjs.com/package/react-avatar-editor) - Similar to Facebook profile picture. Allows you to crop, resize, and rotate an uploaded image. Use for event image upload in event creation.


## API Documentation
* [Backend API Documentation](https://cuevents.docs.apiary.io/) - An external Apiary documenting the endpoints for our application.

## Contributors
**2020**
* **[Jonna Chen](https://github.com/jonnachen)** - Front-End Developer
* **[Woosang Kang](https://github.com/paul-kang-1)** - Back-End Developer
* **[Mena Attia](https://github.com/menaattia)** - Back-End Developer

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
