"""
    This program listens for work messages contiously. 
    
    The bbq_producer.py must run to start sending the messge first
    We want know if (Condition To monitor):
        The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
        
### Name:  Presley Schumacher
### Date:  February 21, 2023
"""
from functools import partial
import pika
import sys
import time
from collections import deque

# Declare deque to store troponin readings for the last hour
# A reading is taken every hour the max. length is 24
# The deque will hold 24 readings to cover the full day's worth of data
troponin_readings = deque(maxlen=24)

# define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    # Decode the message from bytes to string and split it by comma
    message = body.decode()
    parts = message.split(",")
    try:
        # Extract the troponin level from the message and convert it to float
        troponin_level = float(parts[1])
        # Add the troponin level to the deque
        troponin_readings.append(troponin_level)

        # Check if the deque has any readings and if the difference
        # between the max and min values in the deque is greater than or equal to 7.
        # If the condition is met, print a message indicating that the troponin level
        # has increased by 7 or more in the last hour
        if len(troponin_readings) >= 2 and max(troponin_readings) - min(troponin_readings) >= 7:
            print("Alert: Troponin level has increased by 7 or more in the last hour")

        if troponin_level >= 30:
            print("Alert: Troponin level is 30 or higher")
        
        # Acknowledge that the message has been processed and can be removed from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except IndexError:
        print("Error: Message does not contain troponin level")
    except ValueError:
        print("Error: Troponin level is not a valid float")
    
  
# define a main function to run the program
def main(hn: str = "localhost", qn: str = "patient2"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # If there's an error:
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=qn, on_message_callback=callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # If there's an error:
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()
        

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main('localhost', 'patient2')