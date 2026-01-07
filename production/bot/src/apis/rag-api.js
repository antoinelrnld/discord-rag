const axios = require('axios');
const FormData = require('form-data');
const { rag } = require('../config.js');

const rag_api = axios.create({
    baseURL: rag.base_url,
});

exports.healthCheck = async () => {
    try {
        await rag_api.get(rag.health_route, config={timeout: 2000});
        return true;
    } catch (error) {
        console.error('RAG API is currently unavailable');
        return false;
    }
}

exports.inference = async (text) => {
    const form = new FormData();
    form.append('text', text);
    console.log('Sending file to API');

    try {
        const response = await rag_api.post(rag.inference_route, form, {
            headers: form.getHeaders(),
            responseType: 'json',
            timeout: 120000,
        });
        return response.data;
    } catch (error) {
        console.log('Error during inference: ', error.message);
        return null;
    }
}