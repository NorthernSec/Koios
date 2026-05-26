import logging
from koios.config import Config

conf   = Config()
logger = logging.getLogger("koios.admin")

CSP_EXCEMPT_SOURCE_FILES = [
    'sandbox eval code',
    'moz-extension',
]

ENABLE_CSP = not conf._get_property("KOIOS_ADMIN_DISABLE_CSP", False)
DEBUG_CSP  =     conf._get_property("KOIOS_ADMIN_DEBUG_CSP",   False)
