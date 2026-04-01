import os
import secrets

from pathlib import Path


_SECRET_KEY_PATH = "/etc/koios/secret_key"
_DEFAULTS = {
    'secret_key':    ("KOIOS_SECRET_KEY",           None),
    'allowed_hosts': ("KOIOS_ALLOWED_HOSTS",        []),
    'csrf_trusted':  ("KOIOS_CSRF_TRUSTED_ORIGINS", []),
    'media_path':    ("KOIOS_MEDIA_PATH",           'media'),
    'data_path':     ("KOIOS_DATA_PATH",            'data'),
    'log_path':      ("KOIOS_LOG_PATH",             'logs'),
    'database': { 'engine':   ("KOIOS_DB_ENGINE", 'django.db.backends.postgresql'),
                  'name':     ("KOIOS_DB_NAME",   'koios'),
                  'user':     ("KOIOS_DB_USER",   'koios'),
                  'password': ("KOIOS_DB_PASS",   'change_me'),
                  'host':     ("KOIOS_DB_HOST",   'koios_database'),
                  'port':     ("KOIOS_DB_PORT",   '5432')},
    'content_security_policy': { 'default_src': ("CSP_DEFAULT_SRC", "'self'"),
                                 'script_src':  ("CSP_SCRIPT_SRC",  "'self'"),
                                 'style_src':   ("CSP_STYLE_SRC",   "'self'"),
                                 'img_src':     ("CSP_IMG_SRC",     "'self',data:"),
                                 'font_src':    ("CSP_FONT_SRC",    "'self'"),
                                 'report_only': ("CSP_REPORT_ONLY", True)},
    'mime_sniffing':    ("DISABLE_MIME_SNIFFING", True),
    'landingpage_view': ("LANDINGPAGE_VIEW",      None),
}

class Config():
    def _get_property(self, env, default):
        if os.environ.get(env):
            return os.environ.get(env)
        return default

    @property
    def secret_key(self):
        env = self._get_property(*_DEFAULTS['secret_key'])
        if env:
            return env
        if not os.path.exists(_SECRET_KEY_PATH):
            folder = os.path.dirname(_SECRET_KEY_PATH)
            Path(folder).mkdir(parents=True, exist_ok=True)
            key = secrets.token_urlsafe(64)
            open(_SECRET_KEY_PATH, 'w').write(key)
            return key
        else:
            return open(_SECRET_KEY_PATH).read().strip()

    @property
    def allowed_hosts(self):
        hosts = self._get_property(*_DEFAULTS['allowed_hosts'])
        if isinstance(hosts, str):
            hosts = hosts.split(',')
        return hosts

    @property
    def csrf_trusted_origins(self):
        def domain_to_url(d):
            if (d.startswith("https://")  or d.startswith("http://")
                or d.startswith("wss://") or d.startswith("ws://")):
                return d
            return "https://"+d
        hosts = self._get_property(*_DEFAULTS['csrf_trusted'])+self.allowed_hosts
        if isinstance(hosts, str):
            hosts = hosts.split(',')
        hosts = list(set([domain_to_url(h) for h in hosts]))
        return hosts


    @property
    def media_path(self):
        path = self._get_property(*_DEFAULTS['media_path'])
        if not path.startswith("/"): # relative path:
            base  = Path(__file__).resolve().parent.parent
            return base / path
        return Path(path)

    @property
    def data_path(self):
        path = self._get_property(*_DEFAULTS['data_path'])
        if not path.startswith("/"): # relative path:
            base = Path(__file__).resolve().parent.parent
            return base / path
        return Path(path)

    @property
    def log_path(self):
        path = self._get_property(*_DEFAULTS['log_path'])
        if not path.startswith("/"): # relative path:
            base = Path(__file__).resolve().parent.parent
            return base / path
        return Path(path)

    @property
    def database_engine(self):
        return self._get_property(*_DEFAULTS['database']['engine'])

    @property
    def database_name(self):
        return self._get_property(*_DEFAULTS['database']['name'])

    @property
    def database_user(self):
        return self._get_property(*_DEFAULTS['database']['user'])

    @property
    def database_password(self):
        return self._get_property(*_DEFAULTS['database']['password'])

    @property
    def database_host(self):
        return self._get_property(*_DEFAULTS['database']['host'])

    @property
    def database_port(self):
        return self._get_property(*_DEFAULTS['database']['port'])

    @property
    def csp_default_src(self):
        prop = _DEFAULTS['content_security_policy']['default_src']
        return [x.strip() for x in self._get_property(*prop).split(",")]

    @property
    def csp_script_src(self):
        prop = _DEFAULTS['content_security_policy']['script_src']
        return [x.strip() for x in self._get_property(*prop).split(",")]

    @property
    def csp_style_src(self):
        prop = _DEFAULTS['content_security_policy']['style_src']
        return [x.strip() for x in self._get_property(*prop).split(",")]

    @property
    def csp_img_src(self):
        prop = _DEFAULTS['content_security_policy']['img_src']
        return [x.strip() for x in self._get_property(*prop).split(",")]

    @property
    def csp_font_src(self):
        prop = _DEFAULTS['content_security_policy']['font_src']
        return [x.strip() for x in self._get_property(*prop).split(",")]

    @property
    def csp_report_only(self):
        prop = _DEFAULTS['content_security_policy']['report_only']
        return self._get_property(*prop)

    @property
    def disable_mime_sniffing(self):
        return bool(self._get_property(*_DEFAULTS['mime_sniffing']))

    @property
    def landingpage_view(self):
        return self._get_property(*_DEFAULTS['landingpage_view'])
