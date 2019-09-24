from bacdive.utils import check_allow


def get_url(search_value, search_type):

    allowed = [
        'genus',
        'bacdive_id',
        'culture no',
        'species',
        'subspecies',
        'sequence accession number']
    if search_type not in allowed:
        raise ValueError('Search type can only be: ' + ' '.join(allowed))
    print('Retrieving information on: ' + search_value)
    if not check_allow(search_value):
        raise ValueError("Search can only contain letters,"
                         " numbers and white-space only in "
                         "the case os species and subspecies.")
    search_value = search_value.replace(' ', '/')
    g_ = 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/'\
        % (search_value)
    bac_ = 'https://bacdive.dsmz.de/api/bacdive/bacdive_id/%s/'\
        % (search_value.replace('/', ' '))
    cult_ = 'https://bacdive.dsmz.de/api/bacdive/culturecollectionno/%s/'\
        % (search_value.replace('/', ' '))
    sp_ = 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/'\
        % (search_value)
    subsp_ = 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/'\
        % (search_value)
    ssass_ = 'https://bacdive.dsmz.de/api/bacdive/sequence/%s/'\
        % (search_value)
    search_type_links = {'genus': g_,
                         'bacdive_id': bac_,
                         'culture no': cult_,
                         'species': sp_,
                         'subspecies': subsp_,
                         'sequence accession number': ssass_}
    return search_type_links[search_type.lower()]
