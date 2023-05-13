from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Question #부모 디렉터리에 존재하므로 ..붙여주기


def index(request): #request는 장고 프레임워크에 의해 자동으로 전달되는 HTTP 요청 객체
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 (GET방식으로 요청한 URL에서 page의 값을 가져올때 사용)
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')


    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')


    # 조회
    if kw:
        question_list = question_list.filter( #filter 함수안에서 모델속성에 접근할떄는 __이용시 하위 속성에 접근가능.
            Q(subject__icontains=kw) |  # 제목 검색, icontains 대신 contains 사용시 대소문자 구분.
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지 당 10개씩 보여주기(Paginator는 조회된 question_list를 페이징 객체(paginator)로 변환)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so':so}  # <------ so 추가 ,page와 kw가 추가.
    return render(request, 'pybo/question_list.html', context) #템플릿파일


def detail(request, question_id): #전달되는 매개변수가 request외에 question_id가 하나 더 추가
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)#pk는 Question모델의 기본키(Primary Key)인 id를 의미
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)