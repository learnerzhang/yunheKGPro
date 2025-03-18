import json
from user_agents import parse 
from .models import OperationLog, LoginLog  
from django.contrib.auth import authenticate
from django.utils.deprecation import MiddlewareMixin  

LOGIN_URL_EXCLUSIONS = ['/logapp/logs/login/', '/logapp/logs/operation/']  # 白名单，不需要记录日志的URL列表  

class LoggingMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response  
  
    def process_view(self, request, view_func, view_args, view_kwargs): 
        if request.user.is_authenticated:  
            user = request.user  
        else:  
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

        if request.path.startswith('/userapp/userapi/login'):  
            # 记录登录日志  
            self.log_login(request, user)  
  
    def log_login(self, request, user):  
        # 获取登录信息  
        user_agent = request.META.get('HTTP_USER_AGENT')
        user_agent_parsed = parse(user_agent)

        login_data = {  
            'user': user,
            'name': user.name if user else None,
            'username': request.POST.get('username') if user is None else user.username,  
            'ip': request.META.get('REMOTE_ADDR'),  
            'agent': request.META.get('HTTP_USER_AGENT'),  
            'browser': user_agent_parsed.browser.family if user_agent_parsed.browser else None,  # 可以通过解析 HTTP_USER_AGENT 获取浏览器名
            'os': user_agent_parsed.os.family if user_agent_parsed.os else None,      # 可以通过解析 HTTP_USER_AGENT 获取操作系统信息
        }  
        # 保存登录日志  
        LoginLog.objects.create(**login_data)  
  
    def process_response(self, request, response): 
        if request.path not in LOGIN_URL_EXCLUSIONS: 
            # 记录操作日志  
            self.log_operation(request, response)  
        return response  

    def log_operation(self, request, response):
        # 缺少对其他流的支持
        content_type = response.get('Content-Type', '')
        # 检查响应内容是否为文本类型
        if content_type.startswith('text') or 'json' in content_type:
            response_content = response.content
            # 如果是字节类型，先解码
            if isinstance(response_content, bytes):
                response_content = response_content.decode('utf-8')
                try:
                    json_result = json.loads(response_content)
                except json.JSONDecodeError as e:
                    json_result = {}
        else:
            json_result = {}

        user_agent = request.META.get('HTTP_USER_AGENT') 
        user_agent_parsed = parse(user_agent)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # 获取操作信息  
        operation_data = {  
            'user': user,  
            'request_modular': request.path.split('/')[1] if len(request.path.split('/')) > 1 else 'root',  
            'request_path': request.path,  
            'request_body': json.dumps(request.POST.dict() if request.method == 'POST' else {}, ensure_ascii=False),  
            'request_method': request.method,  
            'request_msg': '',    
            'request_ip': request.META.get('REMOTE_ADDR'),  
            'request_browser': user_agent_parsed.browser.family if user_agent_parsed.browser else None,  
            'response_code': str(response.status_code),  
            'request_os': user_agent_parsed.os.family if user_agent_parsed.os else None,    
            'json_result': json_result,  
            'status': '成功' if response.status_code == 200 else '失败',  
        }  

        if request.method == 'POST':
            operation_data['request_msg'] = '创建记录'
        elif request.method == 'GET':
            operation_data['request_msg'] = '读取记录'
        elif request.method == 'PUT' or request.method == 'PATCH':
            operation_data['request_msg'] = '更新记录'
        elif request.method == 'DELETE':
            operation_data['request_msg'] = '删除记录'
        else:
            operation_data['request_msg'] = '未知操作'
            
        # 保存操作日志  
        OperationLog.objects.create(**operation_data)