module.exports = {
  postMCTS: async function(input, endpoint, method){

    const axios = require('axios');

    data = JSON.parse(atob(input))

    if (method == "post") {
      try {
        const response = await axios.post(endpoint, data);
        return `${response.status}`;
      } catch (error) {
        return error.response.status;
      }
    }
  }
};
