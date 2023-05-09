from scrapy import Spider


class BooksToScrapeComSpider(Spider):
    # These below variables are pre-defined names, the Spider expects these names to be the same as below
    name = "books_toscrape_com"
    start_urls = [
        "https://www.eventbrite.com/d/india--bangalore/events--this-weekend/tech-conferences/?page=1"
    ]

    custom_settings = {
        "ZYTE_API_TRANSPARENT_MODE": True,
    }

    def parse(self, response):
        for div in response.css('div.Stack_root__1ksk7'):
            link = div.css('a::attr(href)').get()
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response):
        event_title = response.css('.event-title::text').get()
        date_time = response.css('div.detail__content p span::text').get()
        location = response.xpath('//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[2]/section[2]/div/div/div[2]/p/text()').extract() 
        description = response.css('.eds-text--left p').extract()
        sm_handles = response.css('.css-ojn45 a::attr(href)').extract() 
        yield {
            'title': event_title,
            'date time': date_time,
            'location': location,
            'description': description,
            'social media handles': sm_handles
        }    
        