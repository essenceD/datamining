# Scrapy settings for avito_apts project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'avito_apts'

SPIDER_MODULES = ['avito_apts.spiders']
NEWSPIDER_MODULE = 'avito_apts.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'cookie': 'u=2ony4vlo.otahns.1ds0ev4x87m00; v=1618848508; dfp_group=36; __cfduid=d66425c4d899da09f37125d0c9207b51f1618848509; SEARCH_HISTORY_IDS=1; no-ssr=1; _gcl_au=1.1.1819380585.1618848514; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRUovcG1zeFREWlFPMVNnWTRYL3d4VUwxOTU0Ukx1UnMvMy9nWmVVT0MvNU9NbjQ1b3Y3M3dHV2dsbmFZM1RFWjBQZDRXRURRYzFSSmxLcno5MUlncFprS1lGc0V4K2hZcVF4MFQ3VzdaVHB2Q28xR1VwSkY2eEtNNkVpUkIrNjdQelBGSkRYTjc1SSs2NjJUWGE0cjc2WTNVdm9pN3I5OEw2OUlCYmNwWlJ0eitNWm51dnZNUWgxdmRTdzhNa0xZK2JwMG5Mci9jTjdoL05qdlJqOVo2QnFjaVR1NGNXaitWWFBHQVBiZmw0RW1PcWRBQ2FDd3Z2bXUvNm83c01VYlQiLCJpYXQiOjE2MTg4NDg1MTAsImV4cCI6MTYyMDA1ODExMH0.kVL38RfL-VDs3N7qIZJsVZk3RSN6bkIJnXIXruCy_Qs; _ga=GA1.2.326920196.1618848515; _gid=GA1.2.1737603504.1618848515; _fbp=fb.1.1618848516751.1092695903; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a0df103df0c26013a3bcbb12cfcb09704fa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da78fe44b90230da2aceb6fa41872a5ca4e2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832ee03e8f3f3cc283ec132066b2b40ef76446b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f215eba7933f8fe80842da10fb74cac1eab2da10fb74cac1eabbe1b8fec550f290a09360354b9a5173a3778cee096b7b985bf37df0d1894b088; ft="KIGiHt/XWwxMDHuZ7k5H+kjM7W4KunCeGCaV8Vn1IKSDeUTLveL43o8kSSgdKLKST9ZdHovhJ0fHnNkI3lygmeSu1h741DzLG/f0e/mn7MQ+JUBO9C7XTkRwri+cM1e7WHcsjYeV3PZlEC08MyCKAs6wRPvV7EZhvnw7oY0J75oTXxR3nqyWP3WNfGJBklXD"; buyer_laas_location=633540; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; showedStoryIds=63-62-61-58-50-49-48-47-42-32; lastViewingTime=1618848806462; _dc_gtm_UA-2546784-1=1; buyer_location_id=653240; luri=sankt-peterburg; so=1618848965; buyer_popup_location=653240; sx=H4sIAAAAAAACA6WSQZKjMAxF78K6F7Itg8htgnAMccA9mEQJXbn7iKnqVKe3U%2FJWz19P%2Bqpo69MpXacHxMIRMIvkQoWpOnxVt%2BpQmU%2B%2FLnd77haJwHshEwgxxiwM1UcVqoOpDbUOW0vPj6pLuR1OzbrdBCESRe3JkVm%2Bkd26SLFDBxIp55I5Y4YYC0SUAvwT6bV2JH6Of7pL71cujFS0L%2BZMkl4pHULvrXV1B0duOjLHnhoP2LBzR24x%2BNaa01tcbw0qu99mmic%2BT20BSbFI0fmJMnyzL2yPp0SDXNQQxSgaNUZQA8hY0jsSdySN1Hk%2FmVHbIMeCAChJ6CW1cTW3nk0D0BLZ0KAnMmyCtz5gG5pj6Oqawzv7nwo3y3J30%2BMeQDjvQTIQCpf%2FZDfKDkO%2FLsldcdbEnEEgcdL32lxpl74%2Fp%2FnhdRjUz0USZtbhSinxXYUzO5IcXjvoxS45lZTUQ%2BTMkl52B2O3dbuM403tiqgrPTPU49KjIPiFrOn5%2FAsZS%2FjItAIAAA%3D%3D'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'avito_apts.middlewares.AvitoAptsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'avito_apts.middlewares.AvitoAptsDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'avito_apts.pipelines.AvitoAptsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
DOWNLOAD_DELAY = 2.64004

AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 4.8201
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 11.10503
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
