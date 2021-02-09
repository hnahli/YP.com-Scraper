import scrapy

prof = 'Real Estate Agents'
city = 'Fort Worth, TX'

class YellowPages(scrapy.Spider):
    name = "yp"

    start_urls = [
        'https://www.yellowpages.com/search?search_terms=' + str(prof.replace(' ','+')) + '&geo_location_terms='+str(city)
    ]

    def parse(self, response):

        companies = response.xpath('//*[@class="info"]')
        for company in companies:

            url = company.xpath('h2/a/@href').extract_first()
            yield scrapy.Request(url='https://www.yellowpages.com'+url, callback=self.full_company_detail)
        
        next_page = response.xpath('//*[@id="main-content"]/div[2]/div[4]/ul/li[6]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
                
    def full_company_detail(self, response):

        profiles = response.xpath('//*[@id="bpp"]')
        category = response.css('#business-info > dl > dd.categories ::text').extract_first()
        for profile in profiles:

            yield{
                'Name': profile.xpath('header/article/div/h1/text()').extract()[0],
                'Phone': profile.xpath('header/article/section[2]/div[1]/p/text()').extract()[0],
                'Email': profile.xpath('header/div/a[2]/@href').extract()[0],
                'Address': profile.xpath('header/article/section[2]/div[1]/h2/text()').extract()[0],
                'Website': profile.xpath('header/div/a[1]/@href').extract()[0],
                'Category': category
            }

        