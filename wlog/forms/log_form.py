# wlog/forms/log_form.py
from django import forms
from django.utils import timezone

from ..models.log import Log
from ..models.title import Title


class LogForm(forms.ModelForm):
    """日志条目表单"""
    class Meta:
        model = Log
        fields = ['title', 'log_text']
        widgets = {
            'title': forms.Select(attrs={
                'class': 'form-control',
            }),
            'log_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'please enter the log content...',
            }),
        }
        labels = {
            'title': 'belonging to the title',
            'log_text': 'log content',
        }
        help_texts = {
            'log_text': 'please enter the detailed log content',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 限制标题选择
        self.fields['title'].queryset = Title.objects.all().order_by('-created_at')
        
        # 添加空选项
        self.fields['title'].empty_label = 'please select the title'
        
        # 显示创建时间（只读）
        if self.instance and self.instance.pk:
            created_at_value = self.instance.created_at.strftime('%Y-%m-%d')
            created_at_label = 'log date'
        else:
            created_at_value = 'will be set to today'
            created_at_label = 'log date'
            
        self.fields['created_at_display'] = forms.CharField(
            initial=created_at_value,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            label=created_at_label,
            required=False,
        )

    def clean_log_text(self):
        """验证日志内容"""
        log_text = self.cleaned_data.get('log_text')
        if not log_text or log_text.strip() == '':
            raise forms.ValidationError(
                'the content of the log cannot be empty'
            )
        return log_text.strip()
    
    def save(self, commit=True):
        """保存表单时自动设置 created_at"""
        log = super().save(commit=False)
        
        # 如果是新建且没有设置 created_at，设置为今天
        if not log.pk and not hasattr(log, 'created_at'):
            log.created_at = timezone.now().date()
            
        if commit:
            log.save()
        return log
    
    def clean(self):
        """表单整体验证"""
        cleaned_data = super().clean()
        # 移除对 created_at 的验证
        return cleaned_data