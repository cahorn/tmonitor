import logging
import traceback

LOGGER = logging.getLogger(__name__)

class Notify(object):
    """The base class for all notifier classes."""

    def __init__(self, dst_addr=None, src_addr=None,
            username=None, password=None, cred_file=None):
        """
        Initialize this notifier with the given addresses and authentication
        credentials.
        """
        self.dst_addr = dst_addr
        self.src_addr = src_addr
        self.username = username
        self.password = password
        self.cred_file = cred_file

    def clear_cred(self):
        """Delete the authentication credentials of this notifier."""
        self.username = None
        self.password = None

    def read_cred(self, filename=None):
        """Read authentication credentials from the given file."""
        if filename is None:
            filename = self.cred_file
        try:
            with open(filename) as cred:
                self.username = cred.readline().strip()
                self.password = cred.readline().strip()
        except Exception as e:
            LOGGER.error("Could not read from credential file")
            LOGGER.error(traceback.format_exec())

    def send(self, msg, title=""):
        """
        Send a message via this notifier; intended to be overridden by all
        subclasses.
        """
        pass

