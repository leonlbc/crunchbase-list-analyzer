from company import Company
import os, json

def get_req(dia):
    dirname = os.path.dirname(__file__)
    request_path = os.path.join(dirname, 'saved', 'crunchBaseList' + dia +'.json')

    with open(request_path, 'r') as f:
        request = json.load(f)
    return request

def clean_json(request):
    params = ['identifier', 'founded_on' ,'num_employees_enum', 'categories', 'founder_identifiers',
            'location_identifiers', 'short_description',  'funding_stage', 'last_funding_type', 'last_funding_at',
            'rank_org_company', 'acquisition_announced_on', 'acquirer_identifier']
    cleaned_request = {}
    for i in request['entities']:
        company_request = {}
        company_request['uuid'] = i['uuid']
        i = i['properties']
        for j in params:
            company_request[j] = None
            if j in i:
                if isinstance(i[j], (str, int)):
                    company_request[j] = i[j]
                elif isinstance(i[j], dict):
                    company_request[j] = i[j]['value']
                elif isinstance(i[j], list):
                    attr_to_remove = ['entity_def_id', 'permalink', 'uuid', 'image_id']
                    company_request[j] = []
                    for k in i[j]:
                        for attr in attr_to_remove:
                            try: del k[attr] #Remove dados desnecessarios
                            except KeyError: pass
                        if len(k.keys()) == 1:
                            k = k['value'] #Para formatar ['value':'x'] em ['x'] 
                            company_request[j].append(k)
                        elif len(k.keys()) == 2:
                            for key in k.keys():
                                if key != 'value':
                                    company_request[k[key]] = k['value'] #Para refatorar 'location_ids'
                                    break
                    if company_request[j] == []: del company_request[j]
        
        try: #Em casos sem 'location_ids', atribui None p/ os campos
            if company_request['location_identifiers'] == None:
                for l in ['continent', 'country', 'region', 'city']:
                    company_request[l] = None
        except KeyError: pass

        cleaned_request[company_request['identifier']] = company_request
    return cleaned_request

def companies_array(dia):
    json = clean_json(get_req(dia))
    companies = []
    for i in json:
        companies.append(Company(json[i]))

companies = companies_array()