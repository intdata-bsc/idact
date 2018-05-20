import re
from idact.detail.config.validation.validation_error_message import \
    validation_error_message

# by Jorge Ferreira
# https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
VALID_HOSTNAME_REGEX = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"  # noqa, pylint: disable=line-too-long
VALID_HOSTNAME_REGEX_DESCRIPTION = "RFC 1123 hostname."
__COMPILED = re.compile(pattern=VALID_HOSTNAME_REGEX)


def validate_hostname(hostname):
    """Valid cluster name is a string matching VALID_HOSTNAME_REGEX.
       If hostname is invalid, raises a ValueError or TypeError.
       Otherwise, returns hostname."""
    if not __COMPILED.match(hostname):
        raise ValueError(validation_error_message(
            label='hostname',
            value=hostname,
            expected=VALID_HOSTNAME_REGEX_DESCRIPTION,
            regex=VALID_HOSTNAME_REGEX))
    return hostname
