# wlog/forms/title_form.py
from django import forms
from django.utils import timezone

from ..models.title import Title


class TitleForm(forms.ModelForm):
    """日志标题表单"""

    class Meta:
        model = Title
        fields = ["title_text"]
        widgets = {
            "title_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "please enter the title",
                    "autofocus": True,
                }
            ),
        }
        labels = {
            "title_text": "title",
        }
        help_texts = {
            "title_text": "please enter the log title",
        }

    def __init__(self, *args, **kwargs):
        # 添加创建时间的显示字段（只读）
        if self.instance and self.instance.pk:
            self.fields["created_at_display"] = forms.CharField(
                initial=self.instance.created_at.strftime("%Y-%m-%d"),
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "readonly": True,
                    }
                ),
                label="创建时间",
                required=False,
                help_text="此时间为自动生成，不可修改",
            )
        else:
            self.fields["created_at_display"] = forms.CharField(
                initial="保存时自动生成",
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "readonly": True,
                    }
                ),
                label="创建时间",
                required=False,
                help_text="保存时将自动设置为当前时间",
            )

    def clean_title_text(self):
        """验证标题文本"""
        title_text = self.cleaned_data.get("title_text")
        if not title_text or title_text.strip() == "":
            raise forms.ValidationError("the title cannot be empty")
        if len(title_text) > 200:
            raise forms.ValidationError("the title length cannot exceed 200 characters")
        return title_text.strip()

    def clean_created_at(self):
        """验证创建日期"""
        created_at = self.cleaned_data.get("created_at")
        if created_at and created_at > timezone.now().date():
            raise forms.ValidationError("the creation date cannot be later than today")
        return created_at
