from django import forms
from auctions.models import *

CATEGORIES = [
    ('Home', 'Home'),
    ('Tools', 'Tools'),
    ('Tech', 'Tech'),
    ('Videogames', 'Videogames'),
    ('Garden', 'Garden'),
    ('Music', 'Music'),
    ('Sports', 'Sports'),
    ('Work', 'Work'),
    ('Pets', 'Pets'),
    ('Cars', 'Cars'),
    ('Electronics', 'Electronics'),
]


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['owner', 'status', 'winner', 'currentBid']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control my-3',
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control my-3',
                'placeholder': 'Description'
            }),
            'initialBid': forms.NumberInput(attrs={
                'class': 'form-control my-3',
                'placeholder': 'Initial Bid'
            }),
            'category': forms.Select(choices=CATEGORIES, attrs={
                'class': 'form-control my-3'
            })
        }

        label = False
