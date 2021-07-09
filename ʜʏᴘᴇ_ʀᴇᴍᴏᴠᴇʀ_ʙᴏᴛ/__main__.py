from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import updater, FEEDBACK
from ᴇʟᴍx import ALL_MODULES
from ᴋᴀᴛᴇ import *
from FANCY import *


for module_name in ALL_MODULES:
    imported_module = importlib.import_module("ᴇʟᴍx." + module_name)
    if not hasattr(imported_module, "__element__"):
        imported_module.__element__ = imported_module.__name__
    if not imported_module.__element__.lower() in IMPORTED:
        IMPORTED[imported_module.__element__.lower()] = imported_module
    else:
        pass
    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__element__.lower()] = imported_module
    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)




FEEDBACK.info("Using long polling.")
updater.start_polling(timeout=15, read_latency=4)
FEEDBACK.info("Successfully loaded modules: " + str(ALL_MODULES))
FEEDBACK.info("READY")
updater.idle()