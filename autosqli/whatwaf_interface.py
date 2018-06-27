import json

from autosqli import paths
from autosqli import log

from autosqli.strings import BANNED_TAMPERS
# from autosqli.satanize import remove_thing_url
from autosqli.execute import execute
from autosqli.consts import WHATWAF_VERIFY_NUM, WHATWAF_DEBUG, \
    WHATWAF_DEBUG_REPORT


whatwaf_path = None


def set_whatwaf_path(path):
    global whatwaf_path
    whatwaf_path = path


def whatwaf_url(url):
    """ return WhatWaf's results for a specified url """
    log.debug("Launching WhatWaf on {}".format(url))
    return execute([
        "python", whatwaf_path + 'whatwaf.py', "-u",
        url, "--ra", "--hide", "--json",
        "--verify-num",
        str(WHATWAF_VERIFY_NUM)
    ], paths.WHATWAF_PATH, None, True)


def whatwaf_target(target):
    """ add whatwaf details to a target and returns it """

    # if WHATWAF_DEBUG is True, use the sample WhatWaf report (from consts.py)
    if WHATWAF_DEBUG:
        log.warning("WhatWaf debug mode is on. To disable, " +
                    "check autosqli/target.py ! ( WHATWAF_DEBUG )")

    whatwaf_report = WHATWAF_DEBUG_REPORT if WHATWAF_DEBUG else \
        whatwaf_url(target.url)

    if 'detected website protection' in whatwaf_report:
        target.is_protected_by_waf = True
    else:
        target.is_protected_by_waf = False

    if '-' * 30 in whatwaf_report:
        # extract the json part ( using those " - " )
        gorgeous_report = whatwaf_report.split('-' * 30 + '\n')[1].split(
            '\n' + '-' * 30)[0]

        # load the json
        json_report = json.loads(gorgeous_report)
        # assign the json to the target
        target.is_protected_by_waf = json_report["is protected"]
        target.waf_name = json_report["identified firewall"]
        tampers = json_report["apparent working tampers"] if \
            json_report["apparent working tampers"] is not None else []
        for tamper in tampers:
            if tamper not in BANNED_TAMPERS:
                target.working_tamper.append(tamper)

    # TODO: analyze the report to return the target
    target.whatwaf_report = whatwaf_report
    target.waf_detection_done = True
    return target
