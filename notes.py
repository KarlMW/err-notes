# pylint: disable=locally-disabled,import-error,no-init,too-few-public-methods,broad-except
""" err-notes: Errbot notes plugin
"""

from errbot import BotPlugin, re_botcmd #, webhook, botcmd, arg_botcmd
import os
import datetime

class Notes(BotPlugin):
    """
    err-notes errbot plugin - save all messages to files
    """

    SAVE_DIR = "/srv/notes"
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    SAVE_TEMP = SAVE_DIR + "/tmp"
    if not os.path.exists(SAVE_TEMP):
        os.makedirs(SAVE_TEMP)

    # Setup a counter to make files unique if multiple are created in less
    # than 1 second.
    count = 0
    COUNT_MODULO = 1000

    # Match all messages, except those that start with bot prefix.
    # FIXME: there is probably a variable for the bot prefix - not sure if
    # I can use it here directly, though - might need to match everything
    # here and then check for it inside the function body.
    @re_botcmd(pattern=r".*", prefixed=False)
    def wildcard(self, mess, match):
        """wildcard"""

        if mess.body.strip().startswith("!"):
            return "wildcard ignoring command"

        # Create a unique filename, even if multiple per second.
        # TODO: a fancier implementation would only use the "count" if there
        # were more than one message in any given second.
        self.count = (self.count + 1) % self.COUNT_MODULO
        filename = datetime.datetime.now().strftime( \
                "notes.%Y%m%d_%H%M%S." + str(self.count) + ".txt")

        file_temp = os.path.join(self.SAVE_TEMP, filename)
        file_save = os.path.join(self.SAVE_DIR,  filename)

        with open(file_temp, "a") as notes_file:
            notes_file.write("%s\n" % mess.body)

        # make destination file appear atomically in final location
        try:
            os.rename(file_temp, file_save)
        except Exception as e:
            # FIXME: better message, re-raise error?
            return "error with temp file: %s" % str(e)

        return "wildcard body is '" + mess.body + "' at " + filename

