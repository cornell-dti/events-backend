## Using Heroku
A brief guide to maintaining apps deployed using Heroku.

### Setup:
- Install and Add login credentials for [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Deploying:
[Guide] (https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)
TL;DR: 1. Navigate to your local repo
	   2. Create a new Heroku App `heroku create` 
   	   3. Push changes to Heroku `git push heroku master` (repeat, as necessary)

#### Useful Add-Ons:
- **Database** Heroku Postgres: Simple, relational database.
- **Storage** Bucketeer: Allows for the storage of media using Amazon S3.
- **Logging** PaperTrail: Logs API visits.

_Last updated **12/24/2018**_.
