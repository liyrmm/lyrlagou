# -*- coding: utf-8 -*-
import scrapy


class BossZhipinSpider(scrapy.Spider):
    # 定义spider的名字
    name = 'boss_zhipin'
    # 定义爬取的域
    allowed_domains = ['zhipin.com']
    # 定义入口url
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1']

    # 定义解析规则,这个方法必须叫做parse
    def parse(self, response):
        item = BossItem()
        # 获取页面数据的条数
        node_list = response.xpath("//*[@id=\"main\"]/div/div[2]/ul/li")
        # 循环解析页面的数据
        for node in node_list:
            item["job_title"] = node.xpath(".//div[@class=\"job-title\"]/text()").extract()[0]
            item["compensation"] = node.xpath(".//span[@class=\"red\"]/text()").extract()[0]
            item["company"] = node.xpath("./div/div[2]/div/h3/a/text()").extract()[0]
            company_info = node.xpath("./div/div[2]/div/p/text()").extract()
            temp = node.xpath("./div/div[1]/p/text()").extract()
            item["address"] = temp[0]
            item["seniority"] = temp[1]
            item["education"] = temp[2]
            if len(company_info) < 3:
                item["company_type"] = company_info[0]
                item["company_finance"] = ""
                item["company_quorum"] = company_info[-1]
            else:
                item["company_type"] = company_info[0]
                item["company_finance"] = company_info[1]
                item["company_quorum"] = company_info[2]
            yield item


            # 定义下页标签的元素位置
            next_page = response.xpath("//div[@class=\"page\"]/a/@href").extract()[-1]
            # 判断什么时候下页没有任何数据
            if next_page != 'javascript:;':
                base_url = "https://www.zhipin.com"
                url = base_url + next_page
                yield Request(url=url, callback=self.parse)

