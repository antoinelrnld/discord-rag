const { SlashCommandBuilder } = require('discord.js');
const rag_api = require('../../apis/rag-api.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ask')
        .setDescription('Pose une question')
        .addStringOption(option => option.setName('prompt')
                .setDescription('Le prompt à utiliser')
                .setRequired(true)),
    async execute(interaction) {
        if (!await rag_api.healthCheck()) return await interaction.reply({ content: "API is currently unavailable. Please try again later.", ephemeral: true });

        await interaction.reply({ content: "Processing", ephemeral: true});
        await processText(interaction);
    },
};

const processText = async (interaction) => {
    console.log('Processing text')
    const text = interaction.options.getString('prompt');
    const response = await rag_api.inference(text);
    if (!response) return await interaction.editReply({ content: "Error while processing the text. Please try again later.", ephemeral: true });

    await interaction.deleteReply();
    await interaction.channel.send({
        content: `<@${interaction.user.id}> : __${text}__\n\n ${response.answer}`
    });
}