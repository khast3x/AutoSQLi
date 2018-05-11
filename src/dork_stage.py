from .target import urls_to_targets
from . import log
from . import findDorks           # provides findDorks.dorkLines(dorks)
from .save import current_save


def search_dork(dorks):
    return findDorks.dorkLines(dorks)


def getDorks(args):
    if args.dorkfile is not None and args.dork is not None:
        log.critical("-f (--dork-file) and -d (--dork) are incompatible")
        exit(1)
    elif args.dorkfile is not None:
        exit(2)     # not implemented
        pass        # TODO: accept a dorkfile
    elif args.dorkfile is None and args.dork is None:
        log.debug("interactively querying dork")
        log.info("Enter a dork:")
        dorks = [input("dork: ")]
    else:
        dorks = [args.dork]

    return dorks


def dorkStage(args):
    """ takes args of the program and modify the curren_save properties """
    """ ya, might be a little too sketchy for a function description """

    global current_save
    dorks = getDorks(args)  # get dorks from the args provided
    # get results from the dorks
    urls = search_dork(dorks)

    # convert urls to targets
    targets_to_test = urls_to_targets(urls)
    # append our targets to the current_save
    for target in targets_to_test:
        current_save.targets_to_test.append(target)
