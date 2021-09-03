import logging
import azure.functions as func

import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "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"
ADMIN_EMAIL_ADDRESS = "admalungo@hotmail.com"

def main(msg: func.ServiceBusMessage):
    # logging.info('Python ServiceBus queue trigger processed message: %s',
    #              msg.get_body().decode('utf-8'))
    
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python Service bus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    host = "ndproj3pgsqldb.postgres.database.azure.com"
    dbname = "techconfdb"
    user = "pgadmin@ndproj3pgsqldb"
    password = "ndproj3db!"
    sslmode = "require"

    try:
        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        conn = psycopg2.connect(conn_string)
        logging.info("Connection established")

        cursor = conn.cursor()

        # TODO: Get notification message and subject from database using the notification_id
        cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))

        # print("The number of results: ", cursor.rowcount)

        res_row = cursor.fetchone()

        """ logging.info("SUBJECT: {}".format(res_row[1]))
        logging.info("MESSAGE: {}".format(res_row[0])) """

        # TODO: Get attendees email and name
        cursor.execute("SELECT email, first_name, last_name FROM attendee;")
        result_rows = cursor.fetchall()
        """ logging.info("RESULT: {}".format(result_rows))
        logging.info("NUMBER OF RESULTS (LEN): {}".format(len(result_rows))) """

        # TODO: Loop through each attendee and send an email with a personalized subject
        # attendees = Attendee.query.all()
        for attendee in result_rows:
            subject = '{}: {}'.format(format(attendee[1]), format(res_row[1]))
            
            """ logging.info("*****SENDING EMAIL NOW: {}********".format(subject))
            logging.info("*****EMAIL: {}********".format(attendee[0]))
            logging.info("*****SENDGRID_API_KEY: {}********".format(SENDGRID_API_KEY))
            logging.info("*****ADMIN_EMAIL_ADDRESS: {}********".format(ADMIN_EMAIL_ADDRESS)) """

            email_msg = Mail(
                    from_email=ADMIN_EMAIL_ADDRESS,
                    to_emails=format(attendee[0]),
                    subject=format(res_row[1]),
                    plain_text_content=format(res_row[0]))
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(email_msg)
            
            # logging.info("*****SEND_EMAIL: {}********".format(email_msg))            

            # send_email(format(attendee[0]), subject, format(res_row[0]))
            # logging.info("*****SUBJECT: {}********".format(subject))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        # notification.completed_date = datetime.utcnow()
        completed_date = datetime.utcnow()
        status = 'Notified {} attendees'.format(len(result_rows))
        cursor.execute("UPDATE notification SET completed_date = {}, status = {} WHERE id = {};", (format(completed_date), format(status), format(notification_id)))
        conn.commit()

        # print("Updated 1 row of data")

        # TODO: Close connection
        conn.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(logging.error)

    finally:
        # TODO: Close connection
        cursor.close()

""" def send_email(email, subject, body):
    if not app.config.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message) """