from datetime import datetime
from models.response import Response
import os, json

def get_res(dia, api_name):
    dirname = os.path.dirname(os.path.dirname(__file__))
    response_path = os.path.join(dirname, api_name, 'saved', dia + '.json')

    with open(response_path, 'r') as f:
        response = json.load(f)
    return response

def clean_json(response):
    params = ['identifier', 'founded_on' ,'num_employees_enum', 'categories', 'founder_identifiers',
            'location_identifiers', 'short_description',  'funding_stage', 'last_funding_type', 'last_funding_at',
            'rank_org_company', 'acquisition_announced_on', 'acquirer_identifier']
    cleaned_response = {}
    for i in response['entities']:
        company_response = {}
        company_response['uuid'] = i['uuid']
        i = i['properties']
        for j in params:
            company_response[j] = None
            if j in i:
                if isinstance(i[j], (str, int)):
                    company_response[j] = i[j]
                elif isinstance(i[j], dict):
                    company_response[j] = i[j]['value']
                elif isinstance(i[j], list):
                    attr_to_remove = ['entity_def_id', 'permalink', 'uuid', 'image_id']
                    company_response[j] = []
                    for k in i[j]:
                        for attr in attr_to_remove:
                            #Remove dados desnecessarios
                            try: del k[attr]
                            except KeyError: pass
                        if len(k.keys()) == 1:
                            #Para formatar ['value':'x'] em ['x'] 
                            k = k['value']
                            company_response[j].append(k)
                        elif len(k.keys()) == 2:
                            for key in k.keys():
                                if key != 'value':
                                    #Para formatar 'location_ids'
                                    company_response[k[key]] = k['value'] 
                                    break
                    if company_response[j] == []: del company_response[j]
        
        try: #Em casos sem 'location_ids', atribui None p/ os campos
            if company_response['location_identifiers'] == None:
                for l in ['continent', 'country', 'region', 'city']:
                    company_response[l] = None
        except KeyError: pass

        cleaned_response[company_response['identifier']] = company_response
    return cleaned_response

def response_array(dia, json_response):
    json = clean_json(json_response)
    response = []
    dia = datetime.strptime(dia, '%d%m%Y')
    for i in json:
        response.append(Response(json[i], dia))
    return response
