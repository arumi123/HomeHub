const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const params = {
        TableName: process.env.DYNAMODB_TABLE,
        Item: {
            device_id: event.device_id,
            timestamp: event.timestamp,
            data: event.data
        }
    };

    try {
        await dynamo.put(params).promise();
        return { statusCode: 200, body: 'Data inserted successfully' };
    } catch (error) {
        return { statusCode: 500, body: 'Failed to insert data: ' + error };
    }
};
