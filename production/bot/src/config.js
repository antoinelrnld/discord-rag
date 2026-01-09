const dotenv = require('dotenv');

dotenv.config();

module.exports = {
    token: process.env.DISCORD_BOT_TOKEN,
    rag: {
        base_url: process.env.RAG_API_BASE_URL,
        inference_route: "/invoke",
        health_route: "/health"
    },
    clientId: process.env.DISCORD_BOT_CLIENT_ID
}