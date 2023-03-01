"""
    This program sends a message to a queue on the RabbitMQ server from a CSV File to create alert notifications.
    We are simulating a streaming series of temperature readings from the smoker and 2 different food temperatures
    In the producer, below, we are sending these temperature readings to RabbitMQ
    Author: Presley Schumacher
    Date: February 14, 2023
"""

import pika
import sys
import webbrowser
import csv
import time

# Define the variables
host = 'localhost'
patient1_queue = 'patient1'
patient2_queue = 'patient2'
patient3_queue = 'patient3'
patient4_queue = 'patient4'
data_file = 'patient_troponin_levels.csv'

def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website by using True or False"""
    if show_offer == 'True':
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def send_message():
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.
    """

    # Define reading in the CSV file
    with open(data_file, 'r') as file:
        # Create a csv reader to read per row each new line
        reader = csv.reader(file, delimiter= ',')

        header = next(reader)

        try:
            # create a blocking connection to the RabbitMQ server
            conn = pika.BlockingConnection(pika.ConnectionParameters(host))
            # use the connection to create a communication channel
            ch = conn.channel()
            # delete the queue on starup to clear them before initiating them again
            ch.queue_delete(patient1_queue)
            ch.queue_delete(patient2_queue)
            ch.queue_delete(patient3_queue)
            ch.queue_delete(patient4_queue)

            # use the channel to declare a durable queue
            # a durable queue will survive a  server restart
            # and help ensure messages are processed in order
            # messages will not be deleted until the consumer acknowledges
            ch.queue_declare(queue=patient1_queue, durable=True)
            ch.queue_declare(queue=patient2_queue, durable=True)
            ch.queue_declare(queue=patient3_queue, durable=True)
            ch.queue_declare(queue=patient4_queue, durable=True)
    
            # set the variables for reach column in the row
            for row in reader:
                Time,patient1,patient2,patient3, patient4=row

                # For Smoker, Food_A, and Food_B, the below steps will be followed:
                # use the round() function to round 2 decimal places
                # use the float() function to convert the string to a float
                # use an fstring to create a message from our data
                # prepare a binary message to stream
                # use the channel to publish a message to the queue

                try:
                    patient1 = (float(patient1))
                    patient1_data = f"{Time}, {patient1}"
                    patient1_message = str(patient1_data).encode()
                    ch.basic_publish(exchange="", routing_key=patient1_queue, body=patient1_message)
                    print(f" [x] sent {patient1_message}")
                except ValueError:
                    pass

                try:
                    patient2 = (float(patient2))
                    patient2_data = f"{Time}, {patient2}"
                    patient2_message = str(patient2_data).encode()
                    ch.basic_publish(exchange="", routing_key=patient2_queue, body=patient2_message)
                    print(f" [x] sent {patient2_message}")
                except ValueError:
                    pass    

                try:
                    patient3 = (float(patient3))
                    patient3_data = f"{Time}, {patient3}"
                    patient3_message = str(patient3_data).encode()
                    ch.basic_publish(exchange="", routing_key=patient3_queue, body=patient3_message)
                    print(f" [x] sent {patient3_message}")
                except ValueError:
                    pass 

                try:
                    patient4 = (float(patient4))
                    patient4_data = f"{Time}, {patient4}"
                    patient4_message = str(patient4_data).encode()
                    ch.basic_publish(exchange="", routing_key=patient4_queue, body=patient4_message)
                    print(f" [x] sent {patient4_message}")
                except ValueError:
                    pass   
        
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error: Connection to RabbitMQ server failed: {e}")
            sys.exit(1)
    
        finally:
            # close the connection to the server
            conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below

if __name__ == "__main__":
    # ask the user if they would like to open the RabbitMQ Admmin
    offer_rabbitmq_admin_site('True')
    # Send Message
    send_message()
    # sleep should be for 30 seconds as the assignment calls
    time.sleep(30)