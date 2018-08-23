from bacdive.utils import check_allow

def get_url(search_value,search_type):
    
    allowed=['genus','bacdive id','species','subspecies','sequence accession number']
    if search_type not in allowed:
        raise ValueError('Search type can only be: '+' '.join(allowed))
    print('Retrieving information on: '+search_value)
    if not check_allow(search_value):
        raise ValueError("Search can only contain letters, numbers and white-space only in the case os species and subspecies.")

    search_value=search_value.replace(' ','/')

    if search_type.lower()=='genus':
        return 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/' % (search_value)
    
    elif search_type.lower()=='bacdive id':
        return 'https://bacdive.dsmz.de/api/bacdive/culturecollectionno/%s/' % (search_value.replace('/',' '))
        
    elif search_type.lower()=='species':
        return 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/' % (search_value)
    
    elif search_type.lower()=='subspecies':
        return 'https://bacdive.dsmz.de/api/bacdive/taxon/%s/' % (search_value)
    
    elif search_type.lower()=='sequence accession number':
        return 'https://bacdive.dsmz.de/api/bacdive/sequence/%s/' % (search_value)
    
