from common.utils import pretty_print, setup_logger

log = setup_logger("tests", "tests.log")


def logjson(msg: str, json):
    """
    Invoke `log.info()` with a `msg`, `\\n` and pretty-printed version of `json`.

    """
    pretty_json = pretty_print(json)
    # Stacklevel=2 for displaying calling function instead of this one.
    log.info(msg + "\n" + pretty_json, stacklevel=2)
