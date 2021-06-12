const functions = require("firebase-functions");

const config = functions.config();
exports.exposureNotification = functions.pubsub
  .schedule("*/3 * * * *")
  .region(config.region)
  .timeZone(config.timezone)
  .onRun((context) => {
    console.log("This will be run every 3 mins");
    return null;
  });
