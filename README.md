# web-crawling-naver

  **web-crawling-naver** is an automated bot that gathers and updates web content on [Naver](http://www.naver.com/), which is the biggest Korean search engine, using [selenium](http://selenium-python.readthedocs.io/). The list of sites that **web-crawling-naver** can archive is as follows:

1. [Naver Blog](http://section.blog.naver.com/)
2. [Naver Webtoon](http://comic.naver.com/index.nhn)
3. [Naver News](http://news.naver.com/)
4. [Naver People Search](http://people.search.naver.com/)
5. [Naver Movie](http://movie.naver.com/)

## Installation

#### Selenium
>You can download Python bindings for Selenium from the [PyPI page for selenium package](https://pypi.python.org/pypi/selenium). However, a better approach would be to use [pip](https://pip.pypa.io/en/latest/installing/) to install the selenium package. Python 3.5 has pip available in the [standard library](https://docs.python.org/3.5/installing/index.html). Using *pip*, you can install selenium like this:
```
pip install selenium
```

#### PhantomJS
>[PhantomJS](http://phantomjs.org/download.html) is a headless WebKit scriptable with JavaScript. The latest stable release is version 2.1.

## Usage
### 1. Naver Blog
  If you have a list of queries and wish to retrieve related blog posts of the queries, run **naver_blog_crawler.py**. You can set different date ranges, so you can see what people are saying about certain things during a particular period of time.

![image](https://github.com/TY-Choi/web-crawling-naver/blob/master/naver_blog/naver_blog_crawler.png)

**naver_blog_crawler.py** will generate 2 csv files.  

  * The total number of the related blog posts of each query.
```
"query","starting date","ending date","number of posts"
"도널드 트럼프","20160103","20160103",12
"힐러리 클린턴","20160103","20160103",9
```
  * Actual text of blog posts.
```
"query","date posted","url","text"
"도널드 트럼프","2016.01.03.","http://m.blog.naver.com/didtalk/220586117162","안녕하세요~~ 새해 복 많이 받고 계시죠? 팍팍 받으시기 바랍니다. 위에 나온 두사람의.."
"도널드 트럼프","2016.01.03.","http://m.blog.naver.com/alexj1005/220586546397","'트럼프 역겨워' 공중광고, 루비오 지지자가 만들어 (워싱턴=연합뉴스) 김세진 특파원 = ..."
"힐러리 클린턴","2016.01.03.","http://m.blog.naver.com/y3171190y/220586608443","한 해가 가고 새해가 밝았다. 사실 인간이 달력을 만들어 가지고 그냥 카운트한 결과라고..."
```

### 2. Naver Webtoon
  If you wish to gather data for webtoons that are currently being published on Naver, run **naver_webtoon_crawler.py**. 
  
  ![image](https://github.com/TY-Choi/web-crawling-naver/blob/master/naver_webtoon/naver_webtoon.png)
  
  **naver_blog_crawler.py** will generate 4 csv files.
   * A full list of webtoons that have ever been published on Naver.
```
"id,"publishing_day","genre","title","author","thumbnail","complete","type"
"679519","mon/thu","episode/daily/comic","대학일기","자까","http://thumb.comic.naver.net/webtoon/679519/thumbnail/title_thumbnail_20160601180804_t83x90.jpg","미완결","컷툰"
"20853","tue","episode/daily/comic","마음의소리","조석","http://thumb.comic.naver.net/webtoon/20853/thumbnail/thumbnail_title_20853_83x90.gif","미완결","채널링 작품"
"651673","wed/sat","episode/daily/comic","유미의 세포들","이동건","http://thumb.comic.naver.net/webtoon/651673/thumbnail/title_thumbnail_20151225223121_t83x90.jpg","미완결","컷툰"
"651664","fri","episode/drama/sensibility","밥 먹고 갈래요?","오묘","http://thumb.comic.naver.net/webtoon/651664/thumbnail/title_thumbnail_20150326153630_t83x90.jpg","미완결","컷툰"
"680911","완결","episode/comic","무한도전 릴레이툰","무한도전&웹툰작가","http://thumb.comic.naver.net/webtoon/680911/thumbnail/title_thumbnail_20160617193044_t83x90.jpg","완결","일반"
```
  
   * A list of current webtoon titles mapped to the corresponding webtoon ids.
```
"title","id"
"2016 비명","682803"
"203호 저승사자","670140"
"3P","666537"
"3인칭","682265"
"MZ","675830"
```
   * A list of webtoons episodes with meta data such as the number of recommendations by users, epidsode title, published date, the number of cuts, URL and thumbnail address.
```
"id","recom_num","title","episode","episode_num","date","cut_num","url","thumbnail"
"670140", "70,385", "203호 저승사자", "54. 투철한 신고정신", "54", "20170108", 7, "http://comic.naver.com/webtoon/detail.nhn?titleId=670140&no=54", "http://thumb.comic.naver.net/webtoon/670140/54/inst_thumbnail_20170105183134.jpg"
"670140", "70,385", "203호 저승사자", "53. 옮는거죠 그거", "53", "20170101", 15, "http://comic.naver.com/webtoon/detail.nhn?titleId=670140&no=53", "http://thumb.comic.naver.net/webtoon/670140/53/inst_thumbnail_20161229164019.jpg"
"670140", "70,385", "203호 저승사자", "52. 누가 좀 가져가줘", "52", "20161225", 21, "http://comic.naver.com/webtoon/detail.nhn?titleId=670140&no=52", "http://thumb.comic.naver.net/webtoon/670140/52/inst_thumbnail_20161222200313.jpg"
"670140", "70,385", "203호 저승사자", "51.문 고치는 데만 얼마야", "51", "20161218", 26, "http://comic.naver.com/webtoon/detail.nhn?titleId=670140&no=51", "http://thumb.comic.naver.net/webtoon/670140/51/inst_thumbnail_20161215200001.jpg"
```
   * A list of highly rated comments that are submitted / evaluated by users.
```
"id", "title", "episode", "episode_num", "date", "likes", "rank", "comment_submitted", "up", "down", "text"
169080,"Penguin loves Mev","623화 새들의 집","628","20160728","1","2016-07-28 23:15",2668,24,"이 에피소드를 본 메브 반응이 궁금하네요ㅎㅎ "
169080,"Penguin loves Mev","623화 새들의 집","628","20160728","2","2016-07-28 23:17",1782,17,"메브 이거보고 많이 시무룩하실것같애요ㅜㅜ 그와중에 두분다 너무 어린아이같아서 귀여워요♥"
169080,"Penguin loves Mev","623화 새들의 집","628","20160728","3","2016-07-28 23:21",1352,19,"ㅋㅋㅋㅋㅋ 메브님 기분 좋으라고 새가 된  펭귄님 ㅋㅋㅋㅋㅋㅋ 사실 펭귄도 원래 조류였죠? 서로를 생각하는 모습이 넘 예쁘신 커플 같아요."
```

#### 3. Naver News
  **naver_news.py** will generate 3 csv files.
   * A list of current webtoons mapped to the corresponding webtoon ids.
