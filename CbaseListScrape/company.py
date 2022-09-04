
class Company:

    def __init__(self, company_params):
        self.uuid = company_params['uuid']
        self.year_founded = self.format_year(company_params['founded_on'])
        self.name = company_params['identifier']
        self.founders = company_params['founder_identifiers']
        self.categories = company_params['categories']
        self.short_description = company_params['short_description']
        self.num_employees = self.format_employees(company_params['num_employees_enum'])
        self.last_funding_type = company_params['last_funding_type']
        self.last_funding_at = company_params['last_funding_at']
        self.crunchbase_rank = company_params['rank_org_company']
        self.acquirer = company_params['acquirer_identifier']
        self.announce_date = company_params['acquisition_announced_on']
        self.funding_stage = company_params['funding_stage']
        self.continent = company_params['continent']
        self.country = company_params['country']
        self.region = company_params['region']
        self.city = company_params['city']

    def format_employees(self, code_employee):
        if code_employee == None:
            return code_employee
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
        #Recebe data no formato yyyy-dd-mm e deixa yyyy
        if date != None:
            return date[:4]
        return date

