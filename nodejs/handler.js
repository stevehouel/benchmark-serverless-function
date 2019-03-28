'use strict';

module.exports.hello = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: "Hello Serverless Guys !"
  };

  callback(null, response);
};
