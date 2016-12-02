# pylint: disable=locally-disabled,import-error,no-init,too-few-public-methods
""" Errbot notes plugin
"""

from errbot import BotPlugin, re_botcmd #, webhook, botcmd, arg_botcmd
import os
import datetime

SAVE_DIR = "/srv/notes"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class Notes(BotPlugin):
    """
    Notes plugin - save all messages to files
    """

    # pylint: disable=no-self-use
    @re_botcmd(pattern=r"(.*)")
    def wildcard(self, mess, match):
        """wildcard"""

        filename = datetime.datetime.now().strftime("notes.%Y%m%d_%H%M%S.txt")
        with open(os.path.join(SAVE_DIR, filename), "a") as notes_file:
            notes_file.write("%s\n" % mess.body)

        return "wildcard! '" + match.group(1) \
                + "' body is '" + mess.body + "' at " + filename


