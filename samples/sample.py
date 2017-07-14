# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "samples" package

import os
from xenSplittingService.SplittingService import ContentSplit

def sample():
    splitter = ContentSplit()
    print(os.getcwd())
    print(splitter.partition_expression_set)
    print(splitter.partition_expression_dict)
    print(splitter.company_type_whitelist, type(splitter.company_type_whitelist))
    print(splitter.company_service_type_whitelist, type(splitter.company_service_type_whitelist))
    print(splitter.company_keyword_blacklist, type(splitter.company_keyword_blacklist))
    # splitter.add_company_type('test01', force_add=True)
    # splitter.add_company_type(['test02', 'test03'])
    # splitter.add_company_service_type(['test02'])
    # splitter.add_blocked_company_keyword('test01')
    print(splitter.split('无锡市外服人力资源集团有限公司'))
    print(splitter.split_firmname("CNY 4,900-MERES MEDICAL CONSULTING CO.,LTD"))
    print(splitter.split_msg("CNY 4,900-MERES MEDICAL CONSULTING CO.,LTD"))
    print(splitter.split_firmname('无锡市外服人力资源集团有限公司', enable_english_output=True))
    return 0


if __name__ == '__main__':
    sample()
