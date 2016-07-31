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

## Usage
#### 1. Naver Blog
  If you have a list of queries and wish to retreive their related blog posts, run **naver_blog_crawler.py**. You can set different date ranges, so you can see what people are saying about certain things on a particular period of time.

**naver_blog_crawler.py** will generate 3 files.
  1. Urls  
   It has the list of urls to the related blog posts of a query.
```
"박근혜","박근혜 레임덕","2016.06.24.","20160504","http://blog.daum.net/oursociety/629"
"박근혜","박근혜 레임덕","2016.04.14.","20160504","http://dolmengee.tistory.com/503"
"박근혜","박근혜 레임덕","2016.07.20.","20160504","http://blog.naver.com/hosabi55?Redirect=Log&logNo=220767101946"
"박근혜","박근혜 레임덕","2016.05.20.","20160504","http://sjh25.blog.me/220715122072"
"박근혜","박근혜 레임덕","2016.07.14.","20160504","http://blog.naver.com/ertt2002?Redirect=Log&logNo=220761580768"
"박근혜","박근혜 레임덕","2016.04.14.","20160504","http://blog.naver.com/yukin48?Redirect=Log&logNo=220682949484"
```
  2. Number of posts  
   It has the number of the related posts created of a query. The default setting is to show by each season of a year (ex. 2014 Spring).
```
"박근혜","박근혜 레임덕","20160504",201
"박근혜","박근혜 레임덕","20160601",153
"이명박","이명박 4대강","20160504",265
"이명박","이명박 4대강","20160601",448
```
  3. Blog posts  
   It contains actual text of blog post.
```
"박근혜","박근혜 레임덕","2016.07.20.","20160504","http://m.blog.naver.com/hosabi55/220767101946","박근혜 정부 레임덕 가속화시키는...
"박근혜","박근혜 레임덕","2016.07.14.","20160504","http://m.blog.naver.com/ertt2002/220761580768","'레임덕 박근혜, '정권 안보' 목적 사드 배치'...
```
