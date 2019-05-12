# Devman bot

Python script which is built for examination status notification from
[devman](https://dvmn.org) with a help of [telegram](https://github.com/python-telegram-bot/python-telegram-bot) 
bot. Script is required 2 different telegram bot token for 2 different bots:
1) Main bot which is scanning [devman](https://dvmn.org) long-polling for api for new notifications
2) Logger bot which purpose is to send you all log notifications.

## Requirements
Python >= 3.6, Docker version 18.09.0, DockerDocker-compose version 1.21.0 
are required.

## Usage

* Register at [devman](https://dvmn.org) and obtain an auth token.
* [Get telegram token for your bot](https://core.telegram.org/bots/api).
* Fill .env file with required parameters. Example of .env file is provided.
* Run script with

```bash
docker-compose -f docker-compose-dev.yml up --build
```

## Deploy

There is an easy way to deploy this bot with [heroku](https://www.heroku.com/).
1) Register at [heroku](https://www.heroku.com/).
2) Connect your github account to heroku and deploy app from your repository.
3) Install [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli).
4) Initialize config variables on your application page.
5) Scale your web dynos to 1 or more dynos:
```bash
heroku ps:scale bot=1 --app <your_application_name_here>
heroku heroku logs --tail --app <your_application_name_here>
```


