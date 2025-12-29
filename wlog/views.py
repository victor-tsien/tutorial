# wlog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.utils import timezone

from .models.title import Title
from .models.log import Log
from .forms.title_form import TitleForm
from .forms.log_form import LogForm


class TitleListView(ListView):
    """显示所有标题的列表视图"""
    model = Title
    template_name = 'wlog/titles.html'
    context_object_name = 'titles'
    ordering = ['created_at']

    def get_context_data(self, **kwargs):
        """添加上下文"""
        context = super().get_context_data(**kwargs)
        context['page_title'] = '所有标题'
        context['today'] = timezone.now()
        return context


class LogCreateView(CreateView):
    """创建新日志条目"""
    model = Log
    form_class = LogForm
    template_name = 'wlog/log_form.html'

    def get_success_url(self):
        """成功后的重定向URL - 修正这里！"""
        # 确保使用正确的URL名称
        return reverse('wlog:log_detail', args=[self.object.pk])
    
    def get_context_data(self, **kwargs):
        """添加上下文数据"""
        context = super().get_context_data(**kwargs)
        context['form_title'] = '创建日志'
        context['submit_label'] = '创建'
        
        # 根据是否有title_id参数决定返回链接
        title_id = self.kwargs.get('title_id')
        if title_id:
            context['back_url'] = reverse('wlog:logs_by_title', args=[title_id])
        else:
            context['back_url'] = reverse('wlog:titles')
        return context
    
    def get_initial(self):
        """设置初始数据"""
        initial = super().get_initial()
        initial['created_at'] = timezone.now().date()
        
        # 如果URL中有title_id参数，预选该标题
        title_id = self.kwargs.get('title_id')
        if title_id:
            try:
                title = Title.objects.get(pk=title_id)
                initial['title'] = title
            except Title.DoesNotExist:
                pass
                
        return initial
    
    def form_valid(self, form):
        """表单验证成功后的处理"""
        response = super().form_valid(form)
        messages.success(self.request, '日志创建成功！')
        return response


def titles(request):
    """显示所有的标题"""
    view = TitleListView.as_view()
    return view(request)


def logs_by_title(request, title_id):
    """显示某个标题下的所有日志"""
    title = get_object_or_404(Title, pk=title_id)
    logs = title.logs.all()  # 通过 related_name='logs'获取
    context = {'title': title, 'logs': logs}
    return render(request, 'wlog/logs.html', context)


def log_detail(request, log_id):
    """显示单个日志详情"""
    log = get_object_or_404(Log, pk=log_id)
    context = {'log': log}
    return render(request, 'wlog/log_detail.html', context)