Small application that counts the amount of events added in a redis pub/sub channel.
If a certain treshold of messages over minute is exceeded, a message is published on another pub/sub channel.