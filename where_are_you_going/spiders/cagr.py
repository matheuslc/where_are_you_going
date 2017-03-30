import scrapy
from scrapy.shell import inspect_response

class MySpider(scrapy.Spider):
  name = 'cagr'
  login_url = 'https://sistemas.ufsc.br/login?service=https%3A%2F%2Fcagr.sistemas.ufsc.br%2Fj_spring_cas_security_check&userType=padrao&convertToUserType=alunoGraduacao&lockUserType=1';
  start_urls = [
    'https://cagr.sistemas.ufsc.br/modules/aluno/historicoEscolar/',
  ]

  def start_requests(self):
    return [scrapy.FormRequest(
      self.login_url,
      method='POST',
      formdata={'username': self.username, 'password': self.password},
      callback=self.logged
    )]

  def logged(self, response):
    for url in self.start_urls:
      yield scrapy.Request(url=url, cookies=response.headers.getlist('Set-Cookie'), callback=self.parse)

  def parse(self, response):
    inspect_response(response, self)
