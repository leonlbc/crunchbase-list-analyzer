
class Company:

    def __init__(self, company_params):
        self.year_founded = format_year(company_params['year_founded'])
        self.name = company_params['name']
        self.founders = company_params['founders']
        self.categories = company_params['categories']
        self.short_description = company_params['short_desc']
        self.num_employees = format_employees(company_params['num_employees'])
        self.last_funding_type = company_params['last_funding_type']
        self.locations = company_params['locations']
        '''{
            "country": "",
            "city": ""
        }'''
        self.last_funding_at = company_params['last_funding_at']
        self.crunchbase_rank = company_params['crunchbase_rank']
        self.funding_stage = company_params['funding_stage']
        self.acquisition = company_params['acquisition']
        '''{
            "acquirer": "",
            "announce date": "",
            "funding stage": ""
        }'''

    def format_employees(self, code_employee):
        employees = {
            "c_00001_00010": "1-10",
            "c_00011_00050": "11-50",
            "c_00051_00100": "51-100",
            "c_00101_00250": "101-250",
            "c_00251_00500": "251-500",
            "c_00501_01000": "501-1000",
            "c_01001_05000": "1001-5000",
            "c_05001_10000": "5001-10000",
            "c_10001_max": "10001+"
        }
        return employees[code_employee]
    
    def format_year(self, date):
        #Recebe data no formato 2022-02-02 e deixa apenas 2022
        return date[:4]

