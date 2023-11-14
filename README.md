<h1 align="center">Describer</h1>
<p align="center">An open-source system for automatically describing images sent by users on popular media platforms. Currently supports Discord, support for Slack, Messenger, Telegram, other platforms coming soon!

<center>

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Kav-K/Describer/graphs/commit-activity)  
[![GitHub license](https://img.shields.io/github/license/Kav-K/Describer)](https://github.com/Kav-K/Describer/blob/main/LICENSE)  
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

</center>

# Overview
Automatically describe images sent by users on popular media platforms. Incredibly useful for the visually impaired, Describer will automatically ingest images and using GPT-4-Vision, will interpret the images and convert it into a human-readable textual representation that aims to give users a holistic understanding of the image without needing to be dependent on visually seeing the image itself.

**BOT SETUP SUPPORT AND DEMO SERVER:** [Join Here](https://discord.gg/WvAHXDMS7Q)

# Demo
![Demo](https://im2.ezgif.com/tmp/ezgif-2-9f66aa0e73.gif)

# Setup
Python 3.9 and above are supported

To get up and running with the bot, you need to install the requirements, set up your environment variables, and start the bot.
To install the requirements:
```bash
python3.9 -m pip install -r requirements.txt
```

Then, rename `sample.env` to `.env` and fill it in with your corresponding API keys:
```dotenv
DISCORD_TOKEN="MTE....."
OPENAI_API_KEY="sk-......."
DESCRIBED_CHANNELS="mute-this-testing,blank-test"
ALLOWED_GUILDS="1061370086331523176"
ADMIN_ROLES="Admin"
```
Allowed guilds are comma separated values of guild IDs. You can retrieve guild IDs by right clicking a server on the top left of your discord window and then clicking "Copy ID". Channel names and admin_roles are also case-sensitive and comma separated.

You can get an OpenAI API Key [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key), and learn how to create a discord bot [here](https://www.writebots.com/discord-bot-token/)

# Usage
To start the bot from the root directory of the repo, run:
```bash
python -m discord_service.bot
```

Once other platforms are supported, there will be more commands to run the bots for the other platforms. Moreover, an all-in-one command will be created that runs everything.

Within a discord server only the users that have roles defined in `ADMIN_ROLES` in your environment file are able to turn image descriptions on and off. By default for a server, image descriptions are off. You can turn them on with:

`/describe status:on`

You can turn them off with

`/describe status:off`
