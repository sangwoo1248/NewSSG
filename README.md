# NewSSG
# KoBART를 이용한 뉴스 요약
- 개요: 인터넷의 발달과 스마트폰의 보급으로 인해 종이 신문보다 더 많고 빠르게 인터넷 기사를 접할 수 있으며 하루에 쏟아져 나오는 기사의 양은 상상 이상이다. 하루에도 많은 양의 기사가 게재됨에도 불구하고 현대인은 바쁜 일상 속 신문 한 부 읽기 쉽지 않다. 이러한 어려움을 해결하여 많은 현대인이 더 많은 기사를 접하고 정보를 얻을 수 있도록 도움을 줄 수 있는 신문 요약 정보 제공 웹 페이지를 기획하였으며, 요약된 기사로 신문의 핵심만 빠르게 읽을 수 있도록 페이지를 구성하고 원하는 기사만 본문 전체를 읽을 수 있도록 제공하는 서비스 구현을 목표로 하였다.
- 개발 환경 : AWS EC2, AWS RDS, Ubunutu 20.04, Windows
- 개발 언어 : Python, HTML5, CSS3, JavaScript, SQL
- 개발 도구 : GitHub, Visual Studio Code, Pycharm, Anaconda, MobaXterm
- 사용 기술 : KoBART, BeautifulSoup, Selenium, Django, Bootstrap, NGINX
- DB: MySQL

# 역할(백엔드):
- DB에 있는 기사 제목, 사진, 요약 문, 원문, 원본을 불러와서 웹페이지에 보여줌
- 조회수 구현
- 로그인, 로그아웃, 회원가입 페이지
- AWS EC2와 장고를 연동하고 NGINX와 Gunicorn을 연동 

# 시스템 아키텍쳐
![image](https://user-images.githubusercontent.com/53454667/158965636-ef2a1a78-0890-438e-ab4b-5532bbd2ab54.png)

# 요약 비교
<br>
<img src ="https://user-images.githubusercontent.com/53454667/158966742-b7f9c980-1e17-4ef2-bb92-4dd5b805d611.PNG">
<br>
<h1>벤치마킹<br>
<h3>네이버 요약봇<br>
<h3>AI허브 요약문<br>
<h3>네이트 요약봇<br>
<br>
<h1>참고 자료<br>
<a href = "https://pseudo-lab.github.io/Tutorial-Book/chapters/NLP/Ch1-Introduction.html">
PseudoLab, 자연어 처리 모델 소개 (Introduction to NLP Model)
</a>
<br>
<a href = "https://www.koreascience.or.kr/article/CFKO201408355727285.pdf">박은정, 조성준, “KoNLPy: 쉽고 간결한 한국어 정보처리 파이썬 패키지”, 제 26회 한글 및 한국어 정보처리 학술대회 논문집, 2014.
</a>
<br>
<a href = "https://konlpy.org/ko/latest">KoNLPy:파이썬 한국어 NLP</a><br>
<a href = "https://beta.openai.com/docs/engines/gpt-3">OpenAI, Documentation – Engines</a><br>
<a href = "https://arxiv.org/pdf/1810.04805.pdf&usg=ALkJrhhzxlCL6yTht2BRmH9atgvKFxHsxQ"><br>
Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding”
</a><br>
<a href = "https://wikidocs.net/book/2155">WikiDocs, 딥 러닝을 이용한 자연어 처리 입문</a><br>
<a href = "https://ettrends.etri.re.kr/ettrends/183/0905183002/0905183002.html">
ETRI(전자통신동향분석), 임준호, 김현기, 김영길, 딥러닝 사전학습 언어모델 기술 동향
</a>
