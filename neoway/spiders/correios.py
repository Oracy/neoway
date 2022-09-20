import jsonlines
import logging
import os
import requests
import scrapy
import uuid
from scrapy.http import TextResponse


class CorreiosSpider(scrapy.Spider):
    name = 'correios'
    allowed_domains = ['https://www2.correios.com.br/']
    start_urls = ['https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm']

    def get_all_states(self, response):
        """
        Get all states from dropdown at Correios homepage

        :param response: Brings all data from homepage to scrap
        :return: An array with states e.g.: ['AC', 'AL', ...]
        """
        all_states = response.xpath('//select/option/text()').getall()
        all_states.remove('\r')
        return all_states

    def text_response_result(self, payload):
        post_result = requests.post(self.start_urls[0], data=payload)
        return TextResponse(post_result.url, body=post_result.text, encoding='utf-8')

    def get_all_cep_single_page(self, state):
        """
        Get all information from single state, that have only one page

        :param state: Come from calling function e.g.: 'PA'
        :return: A dict with information as ID, LOCALIDADE and FAIXA DE CEP
        """
        payload = {
            "UF": state,
            "Localidade": ""
        }
        text_response_result = self.text_response_result(payload)
        for row in text_response_result.xpath("(//*[@class='tmptabela'])[position()>1]//tr"):
            if row.xpath('td[3]//text()').extract_first():
                yield {
                    "Id": str(uuid.uuid4()),
                    "Localidade": row.xpath('td[1]//text()').extract_first(),
                    "Faixa de CEP": row.xpath('td[2]//text()').extract_first(),
                }

    def get_all_cep_next_page(self, state, max_next_page):
        """
        Get all information from single state, that have two or more pages

        :param state: Come from calling function e.g.: 'PA'
        :param max_next_page: Receives the max number of cep for single state
        :return: A dict with information as ID, LOCALIDADE and FAIXA DE CEP
        """
        pagini = 0
        pagfim = 50
        while pagini <= max_next_page:
            if pagini == 0:
                payload = {
                    "UF": state,
                }
            else:
                payload = {
                    "UF": state,
                    "Localidade": "**",
                    "Bairro": "",
                    "qtdrow": 50,
                    "pagini": pagini,
                    "pagfim": pagfim,
                }
            text_response_result = self.text_response_result(payload)
            for row in text_response_result.xpath("(//*[@class='tmptabela'])//tr"):
                if row.xpath('td[3]//text()').extract_first():
                    yield {
                        "Id": str(uuid.uuid4()),
                        "Localidade": row.xpath('td[1]//text()').extract_first(),
                        "Faixa de CEP": row.xpath('td[2]//text()').extract_first(),
                    }
            pagini = pagfim + 1
            pagfim = pagfim + 50

    def get_all_pages(self, response):
        """
        Concatenate all data from single and multiple pages into single array

        :param response: Brings all data from homepage to scrap
        :return: An array with all ceps that were captured
        """
        row_details = []
        for state in self.get_all_states(response):
            payload = {
                "UF": state,
                "Location": ""
            }
            text_response_result = self.text_response_result(payload)
            total_items_single_page = text_response_result.xpath("//div[@class='ctrlcontent']//text()")[10].extract()
            if total_items_single_page.strip():
                for cep in self.get_all_cep_single_page(state):
                    row_details.append(cep)
            else:
                max_next_page = int(text_response_result.xpath("//div[@class='ctrlcontent']//text()")[20].extract().split(" ")[4])
                for cep in self.get_all_cep_next_page(state, max_next_page):
                    row_details.append(cep)
        return row_details

    def parse(self, response, **kwargs):
        """
        Start process and save data into a jsonl file

        :param response: Brings all data from homepage to scrap
        :param kwargs: N/A
        :return: Save file with all necessary data
        """
        all_ceps = self.get_all_pages(response)
        try:
            with jsonlines.open(
                    os.path.dirname(os.path.abspath(__file__)) + "/output/data.jsonl", 'w'
            ) as file:
                file.write_all(all_ceps)
            logging.info("File have been saved!")
        except Exception as err:
            logging.error("Error on save file: " + err)