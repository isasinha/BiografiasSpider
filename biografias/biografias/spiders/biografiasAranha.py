import scrapy
 
class BiografiasaranhaSpider(scrapy.Spider):
    name = 'biografiasAranha'
    allowed_domains = ['ebiografia.com']
    start_urls = ['https://www.ebiografia.com/catalogo.php']
      
    def parse(self, response):        
        for link in response.css("#lista-biografias").css("a::attr(href)").getall():
            link_completo = f"https://www.ebiografia.com{link}"
            yield scrapy.Request(link_completo, callback=self.biografia_por_pagina)
        pass
        pagina_atual = response.css('div.paginacao span.current::text').get()
        proxima_pagina = int(pagina_atual) + 1
        link_proxima_pagina = f"https://www.ebiografia.com/catalogo.php?p={proxima_pagina}"
        if link_proxima_pagina is not None:
            link_proxima_pagina = response.urljoin(link_proxima_pagina)
            yield scrapy.Request(link_proxima_pagina, callback=self.parse) 


    def biografia_por_pagina(self, response):
        #/#/#/ Apenas por questão de tamanho, pois algumas biografias são muito extensas, será obtido apenas o primeiro parágrafo
        conteudo = response.css('p::text').get()

        #/#/#/ Caso deseje obter a biografia completa, comentar a linha acima e descomentar as linhas abaixo
        #conteudo = ""
        #for paragrafo in response.css('p::text').getall() : 
        #    conteudo = conteudo + "".join(paragrafo) + '\n'

        infos = response.css('div.infos p::text').getall()
        qtdeInfos = len(infos)
        if  qtdeInfos < 1:
            ocupacao = "não informado"
            data_nascimento = "não informado"
            data_morte = "não informado"
        elif  qtdeInfos == 1:
            ocupacao = infos[0]
            data_nascimento = "não informado"
            data_morte = "não informado"
        elif qtdeInfos == 2:
            ocupacao = infos[0]
            data_nascimento = infos[1]
            data_morte = "não informado"
        else:
            ocupacao = infos[0]
            data_nascimento = infos[1]
            data_morte = infos[2]

        yield {
            'nome': response.css('h1::text').get(),
            'ocupacao': ocupacao,
            'data_nascimento': data_nascimento,
            'data_morte': data_morte,
            'conteudo': conteudo               
        }