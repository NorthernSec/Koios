import logging
from koios.config import Config

conf   = Config()
logger = logging.getLogger("koios.admin")

CSP_EXCEMPT_SOURCE_FILES = [
    'sandbox eval code',
    'moz-extension',
]

def as_bool(value):
    if isinstance(value, str):
        if value.lower() in ['false', 'off', 'no', '0']:
            return False
        else:
            return True
    return bool(value)


ENABLE_CSP = not as_bool(conf._get_property("KOIOS_ADMIN_DISABLE_CSP", False))
DEBUG_CSP  =     as_bool(conf._get_property("KOIOS_ADMIN_DEBUG_CSP",   False))

RUN_DEBUG = as_bool(conf._get_property("KOIOS_ADMIN_RUN_DEBUG", False))
RUN_SSL   = as_bool(conf._get_property("KOIOS_ADMIN_RUN_SSL",   False))
