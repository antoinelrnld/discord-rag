const dotenv = require('dotenv');

dotenv.config();

module.exports = {
    token: process.env.DISCORD_BOT_TOKEN,
    channelId: process.env.DISCORD_CHANNEL_ID,
    mongodb: {
        url: process.env.MONGODB_URL,
        db: process.env.MONGODB_DB,
        collection: process.env.MONGODB_COLLECTION
    }
}