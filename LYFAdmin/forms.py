# -*- coding: utf-8 -*-
from django import forms
from  DjangoUeditor.forms import UEditorField

class MentorDetailContentForm(forms.Form):
    Mentor_Detail = UEditorField("详情", initial="", imagePath='img/%(basename)s_%(datetime)s.%(extname)s', filePath='file/%(basename)s_%(datetime)s.%(extname)s')