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
  2. Number of posts
   It has the number of the related posts created of a query. The default setting is to show by each season of a year (ex. 2014 Spring).
  3. Blog posts
   It contains actual text of blog post.

##### Example:
