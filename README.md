# web-crawling-naver

  **web-crawling-naver** is an automated bot that gathers and updates web content on [Naver](http://www.naver.com/), which is the biggest Korean search engine, using [selenium](http://selenium-python.readthedocs.io/). The list of sites that **web-crawling-naver** can archive is as follows:

1. [Naver Blog](http://section.blog.naver.com/)
2. [Naver Cafe](http://section.cafe.naver.com/)
3. [Naver News](http://news.naver.com/)
4. [Naver Webtoon](http://comic.naver.com/index.nhn)
5. [Naver People Search](http://people.search.naver.com/)
6. [Naver Movie](http://movie.naver.com/)

## Installation

### Selenium
>You can download Python bindings for Selenium from the [PyPI page for selenium package](https://pypi.python.org/pypi/selenium). However, a better approach would be to use [pip](https://pip.pypa.io/en/latest/installing/) to install the selenium package. Python 3.5 has pip available in the [standard library](https://docs.python.org/3.5/installing/index.html). Using *pip*, you can install selenium like this:
```
pip install selenium
```
### PhantomJS
>PhantomJS (phantomjs.org) is a headless WebKit scriptable with JavaScript. The latest stable release is version 2.1.

## Usage
#### 1. Naver Blog
  If you have a list of queries and wish to retreive related blog posts of the queries, run **naver_blog_crawler.py**. You can set different date ranges, so you can see what people are saying about certain things on a particular period of time.

**naver_blog_crawler.py** will generate 3 files.  
  * Urls : It cotains the list of urls to the related blog posts of a query.
```
"박근혜","박근혜 레임덕","2016.05.20.","20160504","http://enlucha.tistory.com/473"
"박근혜","박근혜 레임덕","2016.05.23.","20160504","http://euihyone.blog.me/220717449442"
"박근혜","박근혜 레임덕","2016.06.24.","20160601","http://blog.daum.net/oursociety/629"
"박근혜","박근혜 레임덕","2016.06.11.","20160601","http://blog.naver.com/speconomy?Redirect=Log&logNo=220733414055"
```
  * Number of posts : It has the number of the related blog posts of a query.
```
"박근혜","박근혜 레임덕","20160504",201
"박근혜","박근혜 레임덕","20160601",247
"이명박","이명박 4대강","20160504",265
"이명박","이명박 4대강","20160601",274
```
  * Blog posts : It contains actual text of blog posts.
```
"박근혜","박근혜 레임덕","2016.07.20.","20160504","http://m.blog.naver.com/hosabi55/220767101946","박근혜 정부 레임덕 가속화시키는...
"박근혜","박근혜 레임덕","2016.07.14.","20160504","http://m.blog.naver.com/ertt2002/220761580768","'레임덕 박근혜, '정권 안보' 목적 사드 배치'...
```
#### 2. Naver Webtoon
