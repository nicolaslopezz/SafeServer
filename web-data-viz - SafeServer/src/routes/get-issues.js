var axios = require('axios');
require('dotenv').config();

const username = process.env.ATLASSIAN_USERNAME
const password = process.env.ATLASSIAN_API_KEY
const domain = process.env.DOMAIN

const auth = {
 username: username,
 password: password
};

async function getIssues() {

 try {

   const baseUrl = 'https://' + domain + '.atlassian.net';

   const config = {
     method: 'get',
     url: baseUrl + '/rest/api/2/search',
     headers: { 'Content-Type': 'application/json' },
     auth: auth
   };
   const response = await axios.request(config);
   return response.data;
 } catch (error) {
   console.log('error: ')
   console.log(error.response.data.errors)
 }
}

module.exports = getIssues;