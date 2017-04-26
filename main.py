import requests
from pyquery import PyQuery as pq
import user_agent
import urllib.request as request
import urllib.parse as urlparse
import os
base_url = 'http://pinyin.sogou.com/'


def get_url_content(url):
    back = requests.get(url, headers=user_agent.generate_navigator(os='win'))
    return back.content


def get_page_count(d):
    find_last = d("#dict_page_list ul li:last").prev()
    last_count = find_last.text()
    return int(last_count)+1


def get_all_cate():
    url_list = list()
    content = get_url_content('http://pinyin.sogou.com/dict/cate/index/167').decode("utf-8")
    d = pq(content)
    items = d("#dict_nav_list ul li a").items()
    for v in items:
        href = v.attr("href").strip("/")
        category = href.split("/")[-1]
        temp_cate = {"type": category, "url": base_url+href}
        url_list.append(temp_cate)
    return url_list


def get_file_name(url):
    back = urlparse.parse_qs(url)
    print(back['name'][0])
    return str(back['name'][0]) + ".scel"


def parse_content_list(d):
    items = d(".dict_dl_btn a").items()
    download_url = list()
    for item in items:
        download_url.append(item.attr['href'])
    return download_url


def valid_path(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def do_download_dict(down_list, path):
    for url in down_list:
        try:
            file_name = get_file_name(url)
            file_path = path + file_name
            request.urlretrieve(url, file_path)
        except Exception:
            print(Exception)
            print(url)


def init_content(url, dict_type):
    content = get_url_content(url)
    d = pq(content)
    page_count = get_page_count(d)
    download_dict_url = parse_content_list(d)
    path = "./dict/" + dict_type + "/"
    valid_path(path)
    do_download_dict(download_dict_url, path)
    return page_count

if __name__ == "__main__":
    all_cate = get_all_cate()
    for v in all_cate:
        page_count = init_content(v['url'], v['type'])
        for page in range(2, page_count):
            url = v['url']+"/default/" + str(page)
            print(url)
            init_content(url, v['type'])
