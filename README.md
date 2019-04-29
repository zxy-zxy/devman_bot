# Devman bot

Python script which is built for examination status notification from
[devman](https://dvmn.org) with a help of [telegram](https://github.com/python-telegram-bot/python-telegram-bot) 
bot.

## Requirements
Python >= 3.6 required.

Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

## Usage

* Register at [devman](https://dvmn.org) and obtain an auth token.
* [Get telegram token for your bot](https://core.telegram.org/bots/api).
* Fill .env file with required parameters. Example of .env file is provided.
* Run script with

```bash
python run.py
```