# webtoon-crawling-naver (edited on Feb, 2021)

  **webtoon-crawling-naver** is an automated bot that gathers and updates web content on [Naver](http://www.naver.com/), which is the biggest Korean search engine, using [selenium](http://selenium-python.readthedocs.io/). The code mainly originated from the original implementation ([@taeyoung-choi](https://www.github.com/taeyoung-choi/naver-crawler)).
   The updated version has following difference:
   
1. fixed minor bugs in 2021.

2. edited cutting policy (more elaborately cut by scene).
 Our cutting policy is as follows:
 * Appending every partial image.
 * Detecting edges.
 * Read horizontal pixels of the edge-detected image through top to bottom. (see webtoon_cut_counter.py
   * If (edge info =0 -> >0) ==> beginning of image
   * elif (edge info >0 -> =0) ==> end of image
 
## Installation

#### Selenium
>You can download Python bindings for Selenium from the [PyPI page for selenium package](https://pypi.python.org/pypi/selenium). However, a better approach would be to use [pip](https://pip.pypa.io/en/latest/installing/) to install the selenium package. Python 3.5 has pip available in the [standard library](https://docs.python.org/3.5/installing/index.html). Using *pip*, you can install selenium like this:
```
pip install selenium
```

#### PhantomJS
>[PhantomJS](http://phantomjs.org/download.html) is a headless WebKit scriptable with JavaScript. The latest stable release is version 2.1.


## Usage
>You must set "phantom_path" and "chrome_path" variables in line 401, naver_webtoon_crawler.py. After you can collect webtoon image data by
'''
pytohn naver_webtoon_crawler.py
'''


## Improvement of scene cutting policy
> Our cutting policy shows better collection performance (previous version ([@taeyoung-choi](https://www.github.com/taeyoung-choi/naver-crawler)) lose a lot of cuts).
![image](https://github.com/ckdghk77/naver-crawler/blob/master/fig/edited_cutting_policy.png)
