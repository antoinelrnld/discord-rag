const { MongoClient } = require('mongodb');
const { token, channelIds, mongodb } = require('./config.js');
const { Client, GatewayIntentBits } = require('discord.js');

const MAX_FETCH_LIMIT = 100;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

const mongoClient = new MongoClient(mongodb.url)
const database = mongoClient.db(mongodb.db, { useUnifiedTopology: true });
const collection = database.collection(mongodb.collection);

const fetchAndStoreMessages = async (channelId) => {
    try {
        await mongoClient.connect();

        const channel = await client.channels.fetch(channelId);
        let latestStoredMessageId = await getLatestStoredMessageId(channelId);
        let messagesCollection = null;
        let messagesProcessed = 0;
        
        console.info(`Starting export of messages from channel ${channelId}`);
        do {
            messagesCollection = await fetchMessages(channel, latestStoredMessageId);
            if (messagesCollection && messagesCollection.size > 0) {
                const messages = convertMessagesToObjects(messagesCollection.values());
                await storeMessages(messages);
                latestStoredMessageId = messages.reduce((acc, message) => message.timestamp > acc.timestamp ? message : acc)._id;
            }
        } while (messagesCollection.size === MAX_FETCH_LIMIT);
        console.info(`Successfully exported ${messagesProcessed} messages. Last stored message id: ${latestStoredMessageId}`);
    } catch (error) {
        console.error(error);
    } finally {
        await mongoClient.close();
    }
}

const getLatestStoredMessageId = async (channelId) => {
    try {
        const latestMessage = await collection.find({ 'channel.id': channelId }).sort({ timestamp: -1 }).limit(1).toArray();
        return latestMessage.length ? latestMessage[0]._id : 0;
    } catch (error) {
        console.error('Error while attempting to get latest stored message id:', error);
        throw error;
    }
}

const fetchMessages = async (channel, latestStoredMessageId) => {
    try {
        return await channel.messages.fetch({
            limit: MAX_FETCH_LIMIT,
            cache: false,
            after: latestStoredMessageId
        });
    } catch (error) {
        console.error('Error while fetching messages:', error);
        throw error;
    }
}

const convertMessagesToObjects = (messages) => {
    return Array.from(messages).map(message => ({
            _id: message.id,
            content: message.content,
            timestamp: message.createdTimestamp,
            url: `https://discord.com/channels/${message.guild.id}/${message.channel.id}/${message.id}`,
            channel: { id: message.channel.id },
            author: { id: message.author.id, username: message.author.username },
            guild: { id: message.guild.id }
    }));
}

const storeMessages = async (messages) => {
    try {
        const bulkOps = messages.map(message => ({
            updateOne: {
                filter: { _id: message._id },
                update: { $set: message },
                upsert: true
            }
        }));

        await collection.bulkWrite(bulkOps);
    } catch (error) {
        console.error('Error while attempting to store messages:',error);
        throw error;
    }

}

client.once('ready', async () => {
    for (const channelId of channelIds) await fetchAndStoreMessages(channelId);
    await client.destroy();
});

client.login(token);