from . import base

import email.message
import logging
import traceback
import smtplib

LOGGER = logging.getLogger(__name__)

class Notify(base.Notify):
    """A notifier class that sends notifications via email."""

    def __init__(self, *args, host=None, port=0, **kwargs):
        """ 
        Initialize this notifier with the given addresses and authentication
        credentials.
        """
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def send(self, body, title=""):
        """Send a message via this notifier."""
        # Construct a email notification
        msg = email.message.EmailMessage()
        msg['To'] = self.dst_addr
        msg['From'] = self.src_addr
        msg['Subject'] = title
        msg.set_content(body)
        # Send email notification
        try:
            # Construct connection to email server via SMTP
            smtp = smtplib.SMTP(host=self.host, port=self.port)
            smtp.starttls()
            # Authenticate with email server
            if self.cred_file is not None:
                self.read_cred()
            if self.username is not None and self.password is not None:
                smtp.login(self.username, self.password)
            # Send email notification
            smtp.send_message(msg)
            # Close smtp connection
            smtp.quit()
        except Exception:
            LOGGER.error("Could not send email notification")
            LOGGER.error(traceback.format_exc())
        finally:
            # Clean up
            if self.cred_file is not None:
                self.clear_cred()

