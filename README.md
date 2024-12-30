# Discord-RAG

Easily create a RAG based on your Discord messages.

## Introduction

This repo aims to provide a simple and fast way to create a RAG (Retrieval-Augmented Generation) based on your Discord messages. This allows you to use an LLM that is aware of the context of your messages and can generate responses based on that. The repo also provides code to create a Discord bot that can be used to interact with the model directly in your Discord server. Ask for old informations that were discussed long ago, make summaries, ask questions about you and your friends, have fun with the bot!

To get started, you will need to get through the following steps:

1. [Prerequisites](#prerequisites)
2. [Export your Discord messages](#export-your-discord-messages)
3. [To do](#todo)

> [!WARNING]  
> Keep in mind that the project is in its early stages and is only a prototype for now.

## 1. Prerequisites

- A [Discord Bot Token](https://discordjs.guide/preparations/setting-up-a-bot-application.html#your-bot-s-token)
- [Docker](https://www.docker.com/) (Recommended)
- [Docker Compose](https://docs.docker.com/compose/) (Recommended)
- [Node.js](https://nodejs.org/en/) (If you don't want to use Docker)

## 2. Export your existing Discord messages

First, you will need to export the messages from your Discord server to store them elsewhere. We are going to store them in a MongoDB database.
You can either use your existing MongoDB instance or get one by using the [docker-compose.yml](./docker-compose.yml) file.

> [!IMPORTANT]  
>Don't forget to set the required environment variables in the [.env](./msg_export/src/.env) file.  
>You will need the ID of the channel you want to export the messages from.  
>You can get it by right-clicking on the channel and selecting "Copy ID" in Discord (you will need to enable Developer Mode in the settings).

### Using Docker

Run the following command to start the export process:

First we start the MongoDB instance if needed:
```console
$ cd msg_export
$ docker-compose up
```

Then we start the export process:
```console
$ docker build -t msg_dl_img .
$ docker run msg_dl_img
```

### Using npm
<details>
    <summary>Click to expand</summary>
Run the following command to start the export process:

```console
$ cd msg_export
$ npm install
$ npm start
```
</details>

## TODO