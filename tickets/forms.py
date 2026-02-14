from django import forms
from .models import Ticket, Problem


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('status', 'created_by', 'created_at')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Se o problema não estiver na lista, descreva-o aqui'}),
            'district': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Endereço'}),
        }

    problem = forms.ModelChoiceField(queryset=Problem.objects.all(), required=True,
                                     widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
                                     empty_label='Selecione um problema',
                                     label='Problema')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ensure file fields have consistent classes
        self.fields['photo'].widget.attrs.update({'class': 'form-control form-control-lg', 'accept': 'image/*'})
    
        # labels and required flags in Portuguese
        self.fields['description'].label = 'Descrição'
        self.fields['description'].required = False
        self.fields['district'].label = 'Comunidade'
        self.fields['district'].required = True
        self.fields['address'].label = 'Endereço'
        self.fields['address'].required = True
        self.fields['photo'].label = 'Foto (obrigatória)'
        self.fields['photo'].required = True
    

    def clean(self):
        cleaned = super().clean()
        problem = cleaned.get('problem')
        description = cleaned.get('description')
        if not problem and not description:
            self.add_error('description', 'Se o problema não estiver na lista, especifique-o na descrição.')
        return cleaned
