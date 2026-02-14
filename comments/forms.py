from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva seu comentário... (máximo 500 caracteres)',
                'maxlength': 500
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Comentário'
        self.fields['text'].required = True
        self.fields['photo'].label = 'Foto (opcional)'
        self.fields['photo'].required = False
        self.fields['photo'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text and len(text.strip()) < 3:
            raise forms.ValidationError('O comentário deve ter pelo menos 3 caracteres.')
        return text
