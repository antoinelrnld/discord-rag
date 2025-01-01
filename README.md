# Discord-RAG

This repo aims to provide a simple and fast way to create a RAG (Retrieval-Augmented Generation) based on your Discord messages. This allows you to use an LLM that is aware of the context of your messages and can generate responses based on that. The repo also provides code to create a Discord bot that can be used to interact with the model directly in your Discord server. Ask for old informations that were discussed long ago, make summaries, ask questions about you and your friends, have fun with the bot!

Here is a high-level overview of the architecture we are going to build:
![](./docs/img/discord-rag-architecture.png)

To get started, you will need to get through the following steps:

1. [Prerequisites](#prerequisites)
2. [Export your Discord messages](#export-your-discord-messages)
3. [Run the Indexing Pipeline](#run-the-indexing-pipeline)
4. [Launch the API](#launch-the-api)
5. [Discord Bot](#discord-bot)

> [!WARNING]  
> Keep in mind that the project is in its early stages and is only a prototype for now.

## 1. Prerequisites

- A [Discord Bot Token](https://discordjs.guide/preparations/setting-up-a-bot-application.html#your-bot-s-token)
- An [OpenAI API Key](https://platform.openai.com/settings/)
- [Docker](https://www.docker.com/) (Recommended)
- [Docker Compose](https://docs.docker.com/compose/) (Recommended)

If you don't want to use Docker, you will need the following:
- [Node.js](https://nodejs.org/en/)
- [Python3.10](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/)

## 2. Initial Data Ingestion

![](./docs/img/initial-data-ingestion.png)

First, you will need to export the messages from your Discord server to store them elsewhere. We are going to store them in a MongoDB database.
You can either use your existing MongoDB instance or get one by using the [docker-compose.yml](./docker-compose.yml) file.

> [!IMPORTANT]  
> Don't forget to set the required environment variables in the [.env](./initial_ingestion/src/.env) file.  
> You will need the IDs of the channels you want to export the messages from. (Comma-separated)  
> You can get it by right-clicking on the channel and selecting "Copy ID" in Discord (you will need to enable Developer Mode in the settings).

### Using Docker

First we start the MongoDB instance if needed:
```console
$ docker-compose up mongo -d
```

Then we start the export process:
```console
$ cd initial_ingestion
$ docker-compose run initial_ingestion
```

### Using npm
<details>
    <summary>Click to expand</summary>

```console
$ cd initial_ingestion
$ npm install
$ npm start
```
</details>

> [!NOTE]  
> The extraction process can take a while depending on the number of messages in the channel.  
> You can keep track of the progress by checking the logs.  
> If the process is interrupted, you can restart it and it will continue from where it left off.  
> Once the process is done, you can move on to the next step.

## 3. Run the Indexing Pipeline

![](./docs/img/indexing-pipeline.png)

Now that we have the messages stored in the database, we can start the indexing pipeline. This will create the necessary indexes and embeddings for the messages to be used by the model. We are using a [SemanticChunking](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/a4570f3c4883eb9b835b0ee18990e62298f518ef/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb) strategy to split the messages into chunks. This allows us to group consecutive messages of the same topic together and to have a better representation of the context. At least that's the idea.

> [!IMPORTANT]
> Don't forget to set the required environment variables in the [.env](./production/indexing_pipeline/.env) file.  
> You can let the default values if you want but you will need to set the `OPENAI_API_KEY`.

### Using Docker

```console
$ docker-compose up mongo redis -d # Make sure the MongoDB and Redis instances are running
$ cd production/indexing_pipeline
$ docker-compose run indexing_pipeline
```

### Using Poetry

<details>
    <summary>Click to expand</summary>

```console
$ cd production/indexing_pipeline
$ poetry install
$ poetry run python -m indexing_pipeline
```
</details>

> [!NOTE]
> The indexing process should be relatively fast.  
> Once it's done, you can move on to the next step.

## 4. Launch the API

![](./docs/img/api.png)

We are now ready to launch the API that will allow us to interact with the model. The API receives a prompt from the user, retrieves the most relevant messages from the vector store, includes them in the prompt, and sends it to the model. The model then generates a response based on the context provided.  

> [!IMPORTANT]  
> Don't forget to set the required environment variables in the [.env](./production/api/.env) file.  
> You can let the default values if you want but you will need to set the `OPENAI_API_KEY`.

### Using Docker

```console
$ docker-compose up api -d
```

### Using Poetry

<details>
    <summary>Click to expand</summary>

```console
$ cd production/api
$ poetry install
$ poetry run python -m api
```
</details>

### Using the API

The API provides two endpoints:

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | /health | Check if the API is running | |
| POST | /infer | Generate a response based on the prompt | `text` (Multipart-FormData) |


- `/infer` will return a JSON response with the generated text.
    ```json
    {
        "question": "Tell me what you know about the time we went to the beach last summer.",
        "context": [...],
        "answer": "When you went to the beach last summer, it was a sunny day and you had a lot of fun. You played volleyball and swam in the sea. You also had a picnic and watched the sunset. It was a great day!"
    }
    ```
- `/health` will return a JSON response with the status of the API.
    ```json
    {
        "status": "ok"
    }
    ```

> [!TIP]  
At this point the RAG application is ready to be used. Feel free to integrate it in any application. If you want to interact with the model directly in your Discord server, we provide the code of a Discord bot that you can use in the next section.

## 5. Discord Bot

> [!CAUTION]  
> The real-time data ingestion is not implemented yet.

![](./docs/img/bot.png)

The Discord bot allows you to chat with the model directly in your Discord server. This way, everyone in your server can easily use the RAG application seamlessly. To interact with the bot, use the `/ask` command followed by the question you want to ask. The bot will then generate a response based on the context of the messages it has seen.

> [!IMPORTANT]  
> Don't forget to set the required environment variables in the [.env](./bot/src/.env) file.  
> You will need the `DISCORD_BOT_TOKEN` and the `DISCORD_BOT_CLIENT_ID`.  
> You can find the CLIENT_ID of your bot in the [Discord Developer Portal](https://discord.com/developers/applications) (Named "Application ID").

### Using Docker

```console
$ docker-compose up bot -d
```

### Using npm

<details>
    <summary>Click to expand</summary>

```console
$ cd bot
$ npm install
$ npm start
```
</details>

## Et Voilà!

![](./docs/img/discord-rag-architecture.png)

We built a simple RAG application for Discord! Feel free to contribute to the repo and suggest improvements. For now it is still a proof of concept, there is a lot of room for improvement.  

Once you went through all the steps at least once, you can start the whole application with a single command:

```console
$ docker-compose up -d
```