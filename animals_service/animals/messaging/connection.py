import pika

def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            credentials=pika.PlainCredentials("guest", "guest")
        )
    )
    channel = connection.channel()
    return connection, channel
