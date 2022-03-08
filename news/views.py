from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
import logging
# -2022.02.22 park_jong_won
from .fusioncharts import FusionCharts
from django.db import connection

# -2022.01.24 park_jong_won
logger = logging.getLogger('news')

# -2022.02.07 park_jong_won add {def scrollLog, import datetime} del {def log}
def scrollLog(req):

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')


    if req.method == 'POST':
        if 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

            new_scroll_data = ScrollData(ipaddr=ip, acstime=datetime.now(), url=req.get_full_path(), staytime=req.POST['deltaTime'], scroll=req.POST['scroll'])
            new_scroll_data.save()
        else:
            pass
    else: # get
        session_user = req.session.get('user','guest')
        if session_user == 'guest':
            new_log = Log(ipaddr=ip, acstime=datetime.now(), url=req.get_full_path())
        else:
            new_log = Log(ipaddr=ip, acstime=datetime.now(), url=req.get_full_path(), user_id=req.session.get('user')[0])
        new_log.save()



def author(req, p_id=1):
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    press_query='select * from Press order by p_id'
    sel_press_query=f"""
    select p.p_id, p_name, n.n_id, cd_id, n_title, nd_img, n_input, o_link, nso_id, nso_content
    from Press p
    inner join News n on p.p_id = n.p_id
    inner join N_summarization_one nso on n.n_id = nso.n_id
    where n.p_id = {p_id} and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
    order by n.n_input desc
    """

    press_list = Press.objects.raw(press_query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    sel_press_list = Press.objects.raw(sel_press_query)
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(sel_press_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['press_list'] = press_list
    data['sel_press_list'] = sel_press_list
    data['page_obj'] = page_obj

    response = render(req, "author.html", data)

    return response


def politics(req): # 정치
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 100 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', 1)  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, 10)  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.get_page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "politics.html", data)


def economy(req): # 경제
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 101 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "economy.html", data)


def society(req): # 사회
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 102 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "society.html", data)


def life(req): # 생활문화
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 103 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "life.html", data)


def IT(req): # IT/과학
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 105 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "IT.html", data)


def world(req): # 세계
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select * 
        from News n 
        inner join N_category_detail ncd on n.cd_id = ncd.cd_id 
        inner join N_summarization_one nso on n.n_id = nso.n_id
        where ncd.c_id = 104 and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n.n_id desc
    """
    news_list = News.objects.raw(query)  # models.py Board 클래스의 모든 객체를 board_list에 담음
    # news_list 페이징 처리
    page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(news_list, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    data['page_obj'] = page_obj
    data['news_list'] = news_list

    return render(req, "world.html", data)


def news_post(req, n_id):

    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    query = f"""
        select n.n_id, n.n_title, n.nd_img, nc.n_content, n.o_link, ns_content
        from News n 
        inner join N_content nc on n.n_id = nc.n_id 
        inner join N_summarization ns on n.n_id = ns.n_id
        where n.n_id = {n_id}
    """
    news = News.objects.raw(query)[0]  # models.py Board 클래스의 모든 객체를 board_list에 담음
    data['news'] = news

    # news summarization, news content 줄 바꿈 처리
    ns_c = news.ns_content
    sum_list=[]

    while(ns_c.find('\n') != -1):
        sum_list.append(ns_c[:ns_c.find('\n')])
        ns_c = ns_c[ns_c.find('\n')+1:]

    data['ns_content'] = sum_list

    n_c = news.n_content
    cont_list=[]

    if n_c.find('. ') == -1:
        cont_list.append(n_c)
    else:
        while(n_c.find('. ') != -1):
            cont_list.append(n_c[:n_c.find('. ')+1])
            n_c = n_c[n_c.find('. ')+2:]

    data['n_content'] = cont_list


    try:
        article = get_object_or_404(N_Viewcount, n_id = n_id)
    except:
        article = N_Viewcount.objects.create(n_id=n_id)
    data['article'] = article

    response = render(req, "news_post.html", data)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date -= now
    max_age = 60*60

    cookie_value = req.COOKIES.get('news_post', '')

    if f'_{n_id}_' in cookie_value:
        cookie_value = f'{n_id}_'
    else:
        cookie_value += f'{n_id}_'
        response.set_cookie('news_post', value=cookie_value, max_age=max_age, httponly=True)
        article.hits += 1
        article.save()

    return response


def index(req):
    data = {}

    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')
    
    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    raw = f"select * from News n inner join N_content nc on n.n_id = nc.n_id inner join N_summarization_one nso on n.n_id = nso.n_id  where n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None' order by n_input desc limit 4"
    NC = N_content.objects.raw(raw)

    query = []
    news_list = []
    j = 0
    for i in range(100, 106):
        query.append(want_category(i))
        raw_db = News.objects.raw(query[j])
        news_list.append(raw_db)
        exec(f"data['news_list{i}'] = raw_db")
        exec(f"page{i} = req.GET.get('page', '1')")
        exec(f"paginator{i} = Paginator(news_list[{j}], '10')")
        exec(f"page_obj{i} = paginator{i}.page(page{i})")
        exec(f"data['page_obj{i}'] = page_obj{i}")
        j += 1

    data['banners'] = NC
    
    return render(req, "index.html", data)


def want_category(c_id):
    
    query = f"""
        select n.n_id, p_id, n.cd_id, n_title, nd_img, n_input, o_link, nso_id, nso_content, c_id 
        from News n
        inner join N_summarization_one nso on n.n_id = nso.n_id 
        inner join N_category_detail det on n.cd_id = det.cd_id
        where c_id = {c_id} and n_input != '9999-12-31 00:00:00' and nd_img is not null and nd_img !='None'
        order by n_input desc"""
    return query


def memberinfo(req):
    # memberinfo 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if req.method == 'POST':
        # password 와 password1에 입력된 값이 같다면
        if req.POST['password'] == req.POST['password1'] :
            
            query = f"select id, email from memberinfo where id = '{req.POST['id']}' or email = '{req.POST['email']}'"
            
            id_email = Memberinfo.objects.raw(query)
            try:
                if id_email != None:

                    f_id = id_email[0].id
                    f_email = id_email[0].email

                    if req.POST['id'] == f_id :

                        return render(req, 'memberinfo.html', {'error' : "같은 아이디가 있음"})

                    if req.POST['email'] == f_email:

                        return render(req, 'memberinfo.html', {'error' : "같은 이메일이 있음"})
            except:
                # 객체를 새로 생성
                user = Memberinfo(id=req.POST['id'], password=req.POST['password'], name=req.POST['name'], birth=req.POST['birth'], sex=req.POST['sex'], email=req.POST['email'], phone=req.POST['phone'])
                # DB 저장
                user.save()

                return render(req, 'memberinfo.html', {'save' : "가입완료"})
        else:   
            
            return render(req, 'memberinfo.html', {'error' : "비밀번호 다름"})
    else:

        return render(req, 'memberinfo.html')


def login(req): # 로그인

    #전송 받은 이메일 비밀번호 확인
    u_id = req.POST.get('id')
    psw = req.POST.get('password')

    #유효성 처리
    res_data={}
    if not (u_id and psw):
        res_data = ("모든 칸을 채워주세요.",False)

    else:
        query = f"select id, password from memberinfo where id = '{u_id}'"
        # 기존(DB)에 있는 Memberinfo 모델과 같은 값인 걸 가져온다.
        user = Memberinfo.objects.raw(query)

        if len(user) == 0:
            res_data = ("없는 아이디 입니다.", False)
        else:
            f_password = user[0].password
            f_id = user[0].id
            # 비밀번호가 맞는지 확인한다.
            if f_password == psw:
                #응답 데이터 세션에 값 추가. 수신측 쿠키에 저장됨
                req.session['user'] = f_id, f_password

                res_data = ("환영합니다.", True)

            else:
                res_data = ("비밀번호가 틀렸습니다.", False)

    return res_data


def logout(req):
    req.session.clear()

    return redirect('/')


def search(req):
    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check

            return redirect('index')
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영합니다."

    words = req.GET.get('words', '')

    if words != None:

        query = f"""select * 
                    from News n 
                    inner join N_content nc on n.n_id = nc.n_id 
                    inner join N_summarization_one nso on n.n_id = nso.n_id 
                    where n_title like %s and nd_img is not null and nd_img !='None'
                    order by n_input desc"""

        result = News.objects.raw(query, ["%"+words+"%"])

        page = req.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
        paginator = Paginator(result, '10')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
        page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

        data['result'] = result
        data['page_obj'] = page_obj

    else:
        pass

    data['words'] = words    

    return render(req, 'search.html', data)


def mypage(req):

    data = {}
    scrollLog(req)

    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    if req.method == 'POST':
        if 'id' in req.POST.keys() :

            login_massage, session_user_check = login(req)
            data['login_massage'] = login_massage
            data['session_user_check'] = session_user_check
	        
        elif 'scroll' in req.POST.keys():
            logger.info(f"POST log [IPaddr = {ip}, scroll = {req.POST['scroll']}, deltaTime = {req.POST['deltaTime']}]")

        elif req.session.get('user', 'test'):

            logout(req)
            data['session_user_check'] = False

            return redirect('index')

    else : # GET
        logger.info(f"GET log [IPaddr = {ip},  url = {req.get_full_path()}]]")
        check = req.session.get('user', "test")
        if check == "test": # session값이 없는 경우
            data['session_user_check'] = False
        else:               # session 값이 있는 경우  == 이미 로그인을 한 상태
            data['session_user_check'] = True
            data['login_massage'] = "환영한다!!!"

    user_id = req.session.get('user')[0]
    data['individual_press'] = individual_press(user_id)
    data['individual_category'] = individual_category(user_id)
    data['male_news'], data['female_news'] = gender_news()
    for age, i in zip(age_news(),range(1,6)):
        data[f'gruop{i}_news'] = age
    
    return render(req, 'mypage.html', data)

#  -2022.02.21 park_jong_won
# 사용자(해당 회원)가 많이 읽은 언론사 TOP 5 (현재접속한 회원이 가장 많이 읽은 언론사 5개)
def individual_press(user_id: str):
    cursor = connection.cursor()

    # 1. Log테이블에서 특정 사용자의 URL기록을 얻어온다.
    query_nid_log = f"""select replace(URL,'/news/news_post/','') as nid 
                        from Log 
                        where user_id = '{user_id}' and URL like '/news/news_post/%'"""
    # nid_log_objects = News.objects.raw(query_nid_log)
    cursor.execute(query_nid_log)
    nid_log_rows = cursor.fetchall()

    # 2. n_id를 이용하여 언론사별 조회수 순위 구하기
    limit = 5
    query_pname_count_top = f"""select P.p_name, count(*) 
                                from ({query_nid_log}) as UN 
                                inner join News as N on UN.nid = N.n_id 
                                inner join Press as P on N.p_id = P.p_id 
                                group by P.p_id 
                                order by count(*) DESC limit {limit}"""
    # pname_count_top_objects = News.objects.raw(query_pname_count_top)
    cursor.execute(query_pname_count_top)
    pname_count_top_rows = cursor.fetchall()

    # 얻어온 데이터를 바탕으로 그래프를 그린다.
    graph = {}
    graph['chart'] = {"caption": "많이 본 언론사",
                    "subCaption" : "",
                    "showValues":"1",
                    "showPercentInTooltip" : "0",
                    "numberPrefix" : "$",
                    "enableMultiSlicing":"1",
                    "theme": "fusion"}
    graph['data'] = []
    
    etc_count = len(nid_log_rows)  # 전체 데이터에서 순위권데이터를 빼서 나머지 데이터의 크기를 구하기위한 값
    for pname, count in pname_count_top_rows:
        graph['data'].append({"label": pname, "value": count})
        etc_count -= count
    graph['data'].append({"label": "etc", "value": etc_count})

    pie3d = FusionCharts("pie3d", "individual_press" , "115%", "100%", "individual_press_chart", "json", graph)
    # pie3d = FusionCharts("pie3d"그래프 유형, "ex2"그래프 이름 , "100%"틀의 가로, "400"틀의 세로, "chart-1"HTML태그 id, "json"데이터형식,그래프내용)
    # 그래프내용 예시
    """{
        "chart": {
            "caption": "Recommended Portfolio Split",
            "subCaption" : "For a net-worth of $1M",
            "showValues":"1",
            "showPercentInTooltip" : "0",
            "numberPrefix" : "$",
            "enableMultiSlicing":"1",
            "theme": "fusion"
        },
        "data": [{
            "label": "Equity",
            "value": "300000"
        }, {
            "label": "Debt",
            "value": "230000"
        }, {
            "label": "Bullion",
            "value": "180000"
        }, {
            "label": "Real-estate",
            "value": "270000"
        }, {
            "label": "Insurance",
            "value": "20000"
        }]
    }"""

    return pie3d.render()

# 사용자(해당 회원)가 많이 읽은 카테고리 TOP 5
def individual_category(user_id: str):
    cursor = connection.cursor()

    # 1. Log테이블에서 특정 사용자의 URL안에있는 nid를 얻어온다.
    query_nid_log = f"""select replace(URL,'/news/news_post/','') as nid 
                        from Log 
                        where user_id = '{user_id}' and URL like '/news/news_post/%'"""
    cursor.execute(query_nid_log)
    nid_log_rows = cursor.fetchall()

    # 2. nid를 통해 해당기사의 카테고리를 얻어 카운트한다.
    limit = 5
    query_cdname_count_top = f"""select n_id, NCD.cd_id, NCD.cd_name, count(NCD.cd_id) as count
                                from ({query_nid_log}) as UN
                                inner join News as N on UN.nid = N.n_id
                                inner join N_category_detail as NCD on N.cd_id = NCD.cd_id
                                group by NCD.cd_id
                                order by count(*) DESC limit {limit};"""
    
    cursor.execute(query_cdname_count_top)
    cdname_count_top_rows = cursor.fetchall()

    # 3. 얻어온 데이터를 바탕으로 그래프를 그린다.
    graph = {}
    graph['chart'] = {"caption": "많이 본 카테고리",
                    "subCaption" : "",
                    "showValues":"1",
                    "showPercentInTooltip" : "0",
                    "numberPrefix" : "$",
                    "enableMultiSlicing":"1",
                    "theme": "fusion"
                    }
    graph['data'] = []
    
    etc_count = len(nid_log_rows)  # 전체 데이터에서 순위권데이터를 빼서 나머지 데이터의 크기를 구하기위한 값
    for n_id, cd_id, cd_name, count in cdname_count_top_rows:
        graph['data'].append({"label": cd_name, "value": count})
        etc_count -= count
    graph['data'].append({"label": "etc", "value": etc_count})

    pie3d = FusionCharts("pie3d", "individual_category" , "115%", "100%", "individual_category_chart", "json", graph)

    return pie3d.render()


# 모든 회원들의 성별 많이 읽은 뉴스기사 TOP 5
def gender_news() -> list:
    cursor = connection.cursor()

     # 1. Log테이블에서 모든 회원들의 user_id와 URL안에있는 nid를 얻어온다.
    query_nid_userid_log = f"""select replace(URL,'/news/news_post/','') as nid, user_id 
                                from Log 
                                where URL like '/news/news_post/%' and user_id is not null """
    # cursor.execute(query_nid_userid_log)
    # nid_log_rows = cursor.fetchall()

    # 2. 각각의 기사마다 읽은 회원들의 성별로 카운트한다.
    limit = 5
    query_nid_male_count_top = f"""select sex, nid, N.n_title, count(*) 
                                from ({query_nid_userid_log}) as NUlog 
                                inner join memberinfo as m on NUlog.user_id = m.id
                                inner join News as N on NUlog.nid = N.n_id
                                where sex = '남자' 
                                group by nid 
                                order by count(*) DESC 
                                limit {limit}"""
    
    cursor.execute(query_nid_male_count_top)
    nid_male_count_top_rows = cursor.fetchall()

    query_nid_female_count_top = f"""select sex, nid, N.n_title, count(*) 
                                from ({query_nid_userid_log}) as NUlog 
                                inner join memberinfo as m on NUlog.user_id = m.id 
                                inner join News as N on NUlog.nid = N.n_id
                                where sex = '여자' 
                                group by nid 
                                order by count(*) DESC 
                                limit {limit}"""
    cursor.execute(query_nid_female_count_top)
    nid_female_count_top_rows = cursor.fetchall()

    # 3. 얻어온 데이터를 바탕으로 그래프를 그린다.
    graph_male = {}
    graph_male['chart'] = {"caption": "male",
                        "subCaption" : "남자",
                        "yAxisName" : "조회수",
                        "numberPrefix" : "번",
                        "theme": "fusion"}
    graph_male['data'] = []

    graph_female = {}
    graph_female['chart'] = {"caption": "female",
                            "subCaption" : "여자",
                            "yAxisName" : "조회수",
                            "numberSuffix" : "회",
                            "theme": "fusion"}
    graph_female['data'] = []
    
    for male, female in zip(nid_male_count_top_rows, nid_female_count_top_rows):
        graph_male['data'].append({"label": male[2].replace('"',"'"), "value": male[-1]})
        graph_female['data'].append({"label": female[2].replace('"',"'"), "value": female[-1]})

    # column2d_male = FusionCharts("column2d", "male_news" , "100%", "80%", "male_news_chart", "json", graph_male)
    # column2d_female = FusionCharts("column2d", "female_news" , "100%", "80%", "female_news_chart", "json", graph_female)
    column2d_male = FusionCharts("column2d", "male_news" , "100%", "100%", "gender_news_chart_male", "json", graph_male)
    column2d_female = FusionCharts("column2d", "female_news" , "100%", "100%", "gender_news_chart_female", "json", graph_female)

    return [column2d_male.render(), column2d_female.render()]
    ...

# 회원들의 연령대(10,20,30,40,50)별 많이 읽은 뉴스기사 TOP 5 => 막대 그래프 5개
def age_news() -> list: # 수정 필요!! 2022.02.25 -park
    cursor = connection.cursor()
    # 1. Log에서 모든 회원들의 user_id와 URL에서 nid를 얻어온다.
    query_nid_userid_log = f"""select replace(URL,'/news/news_post/','') as nid, user_id 
                                from Log 
                                where URL like '/news/news_post/%' and user_id is not null """
    
    # 2. 얻어온 데이터로 회원들의 나이대별로 nid를 카운트 한다.
    limit = 5
    nid_age_group_tables = []
    for age_group in range(1,6):
        query_nid_age_group = f"""select N.n_title, user_id, count(*) as count
                                from ({query_nid_userid_log}) as NUlog
                                inner join memberinfo as m on NUlog.user_id = m.id
                                inner join News as N on NUlog.nid = N.n_id
                                where timestampdiff(year, birth, now()) > {age_group*10} and timestampdiff(year, birth, now()) < {(age_group+1)*10}
                                group by nid
                                order by count DESC limit {limit}"""
        cursor.execute(query_nid_age_group)
        nid_age_group_tables.append(cursor.fetchall())


    # 3. 그래프를 그린다.
    # result = {}
    result = []
    for nid_age_group_rows, age_group in zip(nid_age_group_tables, range(1,6)):
        graph = {'chart': {"caption": f"{age_group}0대가 가장 많이 본 뉴스",
                        "yAxisName" : "조회수",
                        "numberSuffix" : "회",
                        "theme": "fusion"},
                'data': []
                }
        for title, user_id, count in nid_age_group_rows:
            graph['data'].append({"label": title.replace('"',"'"), "value": count})

        # result[f'gruop{age_group}_news'] = FusionCharts("column2d", f"gruop{age_group}_news" , "100%", "80%", "age_group_news_chart", "json", graph).render()
        result.append(FusionCharts("column2d", f"gruop{age_group}_news" , "100%", "80%", f"age_group_news_chart_{age_group}", "json", graph).render())

    # graph = {'chart': {"caption": "top 5 news",
    #             "subCaption" : f"{age_group}_group",
    #             "yAxisName" : "조회수",
    #             "numberPrefix" : "$",
    #             "theme": "fusion"},
    #     'data': []
    #     }
        
    # for title, user_id, count in nid_age_group_tables[0]:
    #     graph['data'].append({"label": title.replace('"',"'"), "value": count})   

    # result.append(FusionCharts("column2d", f"gruop1_news" , "100%", "80%", f"age_group_news_chart_1", "json", graph).render())

    return result



