import scrapy
from where_are_you_going.items import Alumni
from scrapy.shell import inspect_response

class Cagr(scrapy.Spider):
  name = 'cagr'
  login_url = 'https://sistemas.ufsc.br/login?service=https%3A%2F%2Fcagr.sistemas.ufsc.br%2Fj_spring_cas_security_check&userType=padrao&convertToUserType=alunoGraduacao&lockUserType=1';
  start_urls = [
    'https://cagr.sistemas.ufsc.br/modules/aluno/espelhoMatricula/',
  ]

  def start_requests(self):
    return [scrapy.FormRequest(
      self.login_url,
      method='GET',
      callback=self.login
    )]

  def login(self, response):
    return scrapy.FormRequest.from_response(
      response,
      formdata={'username': self.username, 'password': self.password},
      callback=self.logged
    )

  def logged(self, response):
    for url in self.start_urls:
      yield scrapy.Request(url=url, headers=response.headers, callback=self.parse)

  def parse(self, response):
    AlumniItem = Alumni(
      name=response.css('td.aluno_info_col4 span::text').extract_first(),
      registry=response.css('td.aluno_info_col2 span::text').extract_first()
    )

    for table in response.css('.rich-table'):
      if table.css('.rich-table-headercell::text').extract_first() == 'Resultados':
        AlumniItem['semester'] = [];

        for index, row in enumerate(table.css('tbody tr')):
          AlumniItem['semester'].append([dict({
            'step': row.css('td:nth-child(1)::text').extract_first(),
            'discipline': row.css('td:nth-child(2)::text').extract_first(),
            'class': row.css('td:nth-child(3)::text').extract_first(),
            'title': row.css('td:nth-child(4)::text').extract_first(),
            'type': row.css('td:nth-child(5)::text').extract_first(),
            'credits': row.css('td:nth-child(6)::text').extract_first(),
            'plan': row.css('td:nth-child(7)::text').extract_first(),
            'time': row.css('td:nth-child(8)::text').extract_first(),
            'note': row.css('td:nth-child(9)::text').extract_first(),
            'frequency': row.css('td:nth-child(10)::text').extract_first()
          })])

    return AlumniItem