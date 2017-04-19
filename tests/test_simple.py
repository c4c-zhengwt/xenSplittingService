# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import xenSplittingService as xsplit

def test_success():
    splitter = xsplit.ContentSplit()
    print(splitter.split_firmname_zh('无锡市外服人力资源有限公司'))
    return 0
