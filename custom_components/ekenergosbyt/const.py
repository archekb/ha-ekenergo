import logging

DOMAIN = "ekenergosbyt"
EKENERO_GET_URL = "https://www.eens.ru/api/home/nls?account="
EKENERO_SEND_URL = "https://lk.eens.ru/info/send_show.php"

LOGGER = logging.getLogger(f"custom_components.{DOMAIN}")