import pandas as pd
import numpy as np
import json

def clean_cat(search_data):
    
            
    """ 
    Combines and cleans all data into multi-index pandas dataframe where columns are DSMZ numbers.
    

    """
    by_id =[]
    for id_ in set([x.split('||')[0] for x in search_data.index]):
        #subset 
        subdf = search_data.loc[[x for x in search_data.index if id_ in x],:].dropna(axis=1)
        # fix col
        subdf.columns = ['DSM_'+id_]
        # fix index 
        subdf.index = ['||'.join(x.split('||')[1:]) for x in subdf.index]
        # where all nan fill nan 
        for in_ in subdf.index:
            if np.sum([1 for v_ in subdf.loc[in_,:][0] \
                    if type(v_) == float and\
                    np.isnan(v_)])==len(subdf.loc[in_,:][0]):
                subdf.loc[in_,:] = np.nan
        # antibtioic resistance
        if 'morphology_physiology||met_antibiotica||ab_resistant' in subdf.index:
            resistant = np.array(list(subdf.loc['morphology_physiology||met_antibiotica||ab_resistant'].values))
        else:
            resistant = np.array([])
        if 'morphology_physiology||met_antibiotica||ab_sensitive' in subdf.index:
            sensitive = np.array(list(subdf.loc['morphology_physiology||met_antibiotica||ab_sensitive'].values))
        else:
            sensitive = np.array([])
        antibiotic = np.zeros(sensitive.shape).astype(str)
        antibiotic[~np.isnan(resistant)] = '+'
        antibiotic[~np.isnan(sensitive)] = '-'
        antibiotic = list(antibiotic.flatten())
        # append combined 
        new_index = 'morphology_physiology||met_antibiotica||ab_res_or_sens'
        subdf.at[new_index, 'DSM_'+id_] = antibiotic
        by_id.append(subdf.sort_index())
    search_data = pd.concat(by_id,axis=1)
    #split multi index
    nindex = pd.MultiIndex.from_tuples([(x.split('||')) for x in search_data.index], 
                            names=['Section', 'Subsection','Field'])
    search_data.index = nindex
    return search_data

def flatten_df(results):

    flat_sections=[]
    flat_subsections=[]
    flat_field_id=[]
    flat_fields=[]

    for section_,sub_section_lists in results.items():

        #if not refrences then dict
        if isinstance(sub_section_lists, dict):
            for sub_section,sub_section_list in sub_section_lists.items():
                if sub_section=='straininfo_link': # pragma: no cover
                    continue 
                for field_dict in sub_section_list:
                    for field_id,field in field_dict.items():
                        if field==None:
                            field=np.nan
                        flat_sections.append(section_)
                        flat_subsections.append(sub_section)
                        flat_field_id.append(field_id)
                        flat_fields.append(field)
        #refs  
        elif isinstance(sub_section_lists, list): # pragma: no cover
            if section_=='references':
                combine_ref={'ID_reference':[],'reference':[]}
                for ref_count_,sub_section_dict in enumerate(sub_section_lists):
                    #flattend refrences
                    for field_id,field in sub_section_dict.items():
                        if field==None: # pragma: no cover
                            continue
                        combine_ref[field_id].append(field)
                for field_id,field in combine_ref.items():
                    flat_sections.append(section_)
                    flat_subsections.append('refs')
                    flat_field_id.append(field_id)
                    flat_fields.append(field)
            else: # pragma: no cover
                for ref_count_,sub_section_dict in enumerate(sub_section_lists):
                    for field_id,field in sub_section_dict.items():
                        if field==None:
                            field=np.nan
                        flat_sections.append(section_)
                        flat_subsections.append('refs')
                        flat_field_id.append(field_id)
                        flat_fields.append(field)

    return pd.DataFrame([flat_sections,flat_subsections,flat_field_id,flat_fields]
                 ,index=['Section','Subsection','Field_ID','Field']).T


