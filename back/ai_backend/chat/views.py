from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import ollama
from openai import OpenAI
import json
import requests
from bs4 import BeautifulSoup
from .models import ChatMessage
    
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
class ChatView(APIView):
    def get(self, request):
        try:
            res = ollama.list()
            # 提取所有模型名
            model_names = [model.model for model in res.models]
            return Response({"models": model_names}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocalSolveView(APIView):
    def post(self, request):
       
        try:
            # 从 request.data 中获取模型名称和对话信息
            data = request.data
            model_name = data.get("model")
            inf = data.get("inf")
            website = inf.get("website")
            problem=inf.get("problem")
            code=inf.get("code")
            runResult=inf.get("runResult")
            examples=inf.get("examples")
            
            examples_str = json.dumps(examples, ensure_ascii=False) if examples else "无样例"
            response=ollama.generate(model=model_name,prompt='你是一个C语言助教系统，下面是一个C语言编程题目：'+problem+'，学生的代码如下：'+code+'，运行结果是：'+runResult+'，题目的样例输入输出为：'+examples_str+'，请你在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。',stream=False,options={"max_tokens": 100 })
            # response=ollama.generate(model=model_name,prompt='who are you',stream=False,options={"temperature": 0.7,"max_tokens": 100 })
            # 返回成功响应
            # print(response)
            ChatMessage.objects.update_or_create(
                website=website,
                defaults={
                    "model_name": model_name,
                    "problem": problem,
                    "code": code,
                    "runResult": runResult,
                    "examples": examples,
                    "ans": response.response,
                    "messages": [],
                }
            )
            return Response( response,status=status.HTTP_200_OK)
        except Exception as e:
            # 捕获异常并返回错误信息
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class OnlineSolveView(APIView):
    def post(self, request):
        modellist = {'Deepseek-V3':'https://api.deepseek.com'}
        
        data = request.data
        model = data.get("model")
        apikey = model.get("apikey")
        modelName = model.get("modelName")
        baseurl = modellist.get(modelName)
        if not baseurl:
            return Response({"error": "模型名称不正确"}, status=status.HTTP_400_BAD_REQUEST)
        if not apikey:
            return Response({"error": "apikey不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        
        inf = data.get("inf")
        website = inf.get("website")
        problem=inf.get("problem")
        code=inf.get("code")
        runResult=inf.get("runResult")
        examples=inf.get("examples")
        examples_str = json.dumps(examples, ensure_ascii=False) if examples else "无样例"
        client = OpenAI(api_key=apikey, base_url=baseurl)
        try:
            response=client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个C语言助教系统,下面会给出学生对于一道编程题的解答，请你在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。"},
                    {"role": "user", "content": '你是一个C语言助教系统，下面是一个C语言编程题目：'+problem+'，学生的代码如下：'+code+'，运行结果是：'+runResult+'，题目的样例输入输出为：'+examples_str+'，请你在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。'}
                ],
                stream=False,
                
            )
            ChatMessage.objects.update_or_create(
                website=website,  
                defaults={
                    "model_name": modelName,
                    "problem": problem,
                    "code": code,
                    "runResult": runResult,
                    "examples": examples,
                    "ans": response.choices[0].message.content,
                    "messages": [],
                }
            )
            return Response( response.choices[0].message.content,status=status.HTTP_200_OK)
        except Exception as e:
            # 捕获异常并返回错误信息
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocalChatView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            inf = data.get("inf")
            website = inf.get("website")  # 前端需传递唯一标识 website
            inputmessage = inf.get("inputMessage", "")
            chat = ChatMessage.objects.get(website=website)
            problem = chat.problem
            code = chat.code
            runResult = chat.runResult
            examples = chat.examples
            examples_str = json.dumps(examples, ensure_ascii=False) if examples else "无样例"
            ans = chat.ans
            messages = chat.messages
            messages_str = json.dumps(messages, ensure_ascii=False) if messages else "无消息"
            model_name = chat.model_name

            response=ollama.generate(model=model_name,prompt='你是一个C语言助教系统，下面是一个C语言编程题目：'+problem+'，学生的代码如下：'+code+'，运行结果是：'+runResult+'，题目的样例输入输出为：'+examples_str+'，你已经给出了回答：'+ans+'你和学生后续的对话历史如下：'+messages_str+'学生最新的对话是：'+inputmessage+'请根据题目信息和回答历史，解决学生最新的提问，保证在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。',stream=False,options={"max_tokens": 100 })
            chat.messages.append({"role": "user", "content": inputmessage})
            chat.messages.append({"role": "assistant", "content": response.response})
            chat.save()  # 保存更新后的消息记录
            # 返回成功响应
            # print(response)
            return Response( response,status=status.HTTP_200_OK)
        except Exception as e:
            # 捕获异常并返回错误信息
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class OnlineChatView(APIView):
    def post(self, request):
        modellist = {'Deepseek-V3':'https://api.deepseek.com'}
        data = request.data
        inf = data.get("inf")
        website = inf.get("website")
        inputmessage = inf.get("inputMessage", "")
    
        chat = ChatMessage.objects.get(website=website)
        model = data.get("model")
        apikey = model.get("apikey")
        modelName = model.get("modelName")
        baseurl = modellist.get(modelName)
        if not baseurl:
            return Response({"error": "模型名称不正确"}, status=status.HTTP_400_BAD_REQUEST)
        if not apikey:
            return Response({"error": "apikey不能为空"}, status=status.HTTP_400_BAD_REQUEST)
       
        problem = chat.problem
        code =  chat.code or ""
        runResult = chat.runResult
        examples = chat.examples
        examples_str = json.dumps(examples, ensure_ascii=False) if examples else "无样例"
        ans = chat.ans
        messages = chat.messages
        messages_str = json.dumps(messages, ensure_ascii=False) if messages else "无消息"
        
        client = OpenAI(api_key=apikey, base_url=baseurl)
        try:
            response=client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个C语言助教系统,下面会给出学生对于一道编程题的解答，请你在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。"},
                    {"role": "user", "content": '你是一个C语言助教系统，下面是一个C语言编程题目：'+problem+'，学生的代码如下：'+str(code)+'，运行结果是：'+runResult+'，题目的样例输入输出为：'+examples_str+'，你已经给出了回答：'+ans+'你和学生后续的对话历史如下：'+messages_str+'学生最新的对话是：'+inputmessage+'请根据题目信息和回答历史，解决学生最新的提问，保证在不告诉学生正确答案的前提下，给出一些提示和建议，帮助学生更好地理解题目和修改代码。'}
                ],
                stream=False,
            )
            chat.messages.append({"role": "user", "content": inputmessage})
            chat.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            chat.save()  # 保存更新后的消息记录
            
            return Response( response.choices[0].message.content,status=status.HTTP_200_OK)
        except Exception as e:
            # 捕获异常并返回错误信息
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class GetProblemView(APIView):
    def post(self, request):
        url = request.data.get("url")
        cookies = request.data.get("cookies")  # 从前端获取 Cookie 字符串
        codeurl = url.replace("view.php", "history.php")  # 替换 URL 中的 view.php 为 history.php
        
        if not url or not cookies:
            return Response({"error": "URL 和 Cookies 不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 将前端传递的 Cookie 字符串解析为字典
            cookies_dict = {}
            for cookie in cookies.split(";"):
                if "=" in cookie:  # 检查是否包含 "="
                    key, value = cookie.strip().split("=", 1)
                    cookies_dict[key] = value
                else:
                    print(f"无效的 Cookie: {cookie.strip()}")  # 可选：记录无效的 Cookie

            # 使用手动登录后的 Cookie 发送请求
            response = requests.get(url, cookies=cookies_dict)
            response.raise_for_status()

            coderesponse = requests.get(codeurl, cookies=cookies_dict)
            coderesponse.raise_for_status()
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            codesoup = BeautifulSoup(coderesponse.text, 'html.parser')
            # 提取题目描述部分的文字信息
            problem_text = ""
            problem_md = ""
            code = ""
            code_textarea = codesoup.find('textarea', id='code')  # 查找 id="code" 的 <textarea>
            if code_textarea:
                code = code_textarea.get_text(strip=True)  # 提取代码内容

            # 假设题目描述在 <p> 标签中，带有特定的 class
            paragraphs = soup.find_all('p', class_='md-end-block')
            for p in paragraphs:
                problem_text += p.get_text(strip=True)  # 提取纯文本
                problem_md += str(p)  # 提取 Markdown 格式内容

            # 提取输入样例和输出样例
            input_samples = []
            output_samples = []

            # 找到所有输入样例
            input_elements = soup.find_all('td', class_='programming-io cell c1')
            for element in input_elements:
                div = element.find('div')  # 仅提取 <div> 内的内容
                if div:
                    input_data = div.get_text(strip=True).replace("↵", "\n")  # 替换换行符
                    input_samples.append(input_data)

            # 找到所有输出样例
            output_elements = soup.find_all('td', class_='programming-io cell c2')
            for element in output_elements:
                div = element.find('div')  # 仅提取 <div> 内的内容
                if div:
                    output_data = div.get_text(strip=True).replace("↵", "\n")  # 替换换行符
                    output_samples.append(output_data)

            # 整合输入和输出样例
            examples = []
            for i in range(min(len(input_samples), len(output_samples))):
                examples.append({
                    "input": input_samples[i],
                    "output": output_samples[i]
                })

            # 返回提取的内容
            return Response({
                "problem_text": problem_text,
                "problem_md": problem_md,
                "code": code,
                "examples": examples
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            # 捕获 HTTP 请求错误
            return Response({"error": f"请求失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # 捕获其他异常
            return Response({"error": f"解析失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
