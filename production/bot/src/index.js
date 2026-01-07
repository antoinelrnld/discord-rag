const { Client, GatewayIntentBits, Events, Collection } = require('discord.js');
const { token } = require('./config.js');
const fs = require('node:fs');
const path = require('node:path');
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.commands = new Collection();

const foldersPath = path.join(__dirname, 'commands');
const commandFolders = fs.readdirSync(foldersPath);

for (const folder of commandFolders) {
    const commandsPath = path.join(foldersPath, folder);
    const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith(".js"));
    for (const file of commandFiles) {
        const filePath = path.join(commandsPath, file);
        const command = require(filePath);

        if ('data' in command && 'execute' in command) {
            client.commands.set(command.data.name, command);
        } else {
            console.error(`[WARNING] The command at ${filePath} is missing a requires "data" or "execute" property.`);
        }
    }
}

client.on(Events.InteractionCreate, async interaction => {
    console.log(`Received interaction ${interaction.id}`);
    if (!interaction.isChatInputCommand()) return;

    console.log(`Received command ${interaction.commandName}`);
    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) {
        console.error(`No command matching ${interaction.commandName} was found.`);
    }

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        if (interaction.replied || interaction.deferred) {
            await interaction.followUp({
                content: 'There was an error while executing this command!',
                ephemeral: true
            });
        } else {
            await interaction.reply({
                content: 'There was an error while executing this command!',
                ephemeral: true
            });
        }
    }
});

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
})

client.login(token);