"""
 Dictzone

 @website     https://dictzone.com/
 @provide-api no
 @using-api   no
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from urllib.parse import urljoin
from lxml import html
from searx.utils import eval_xpath


engine_type = 'online_dictionnary'
categories = ['general']
url = 'https://dictzone.com/{from_lang}-{to_lang}-dictionary/{query}'
weight = 100

results_xpath = './/table[@id="r"]/tr'
https_support = True


def request(query, params):
    params['url'] = url.format(from_lang=params['from_lang'][2],
                               to_lang=params['to_lang'][2],
                               query=params['query'])

    return params


def response(resp):
    results = []

    dom = html.fromstring(resp.text)

    for k, result in enumerate(eval_xpath(dom, results_xpath)[1:]):
        try:
            from_result, to_results_raw = eval_xpath(result, './td')
        except:
            continue

        to_results = []
        for to_result in eval_xpath(to_results_raw, './p/a'):
            t = to_result.text_content()
            if t.strip():
                to_results.append(to_result.text_content())

        results.append({
            'url': urljoin(resp.url, '?%d' % k),
            'title': from_result.text_content(),
            'content': '; '.join(to_results)
        })

    return results
