from django import forms
from .models import AuctionListing

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a description for your listing...'}),
        }

    # Ensure that fields are not left blank
    def clean_starting_bid(self):
        starting_bid = self.cleaned_data['starting_bid']
        if starting_bid <= 0:
            raise forms.ValidationError("The starting bid must be a positive number.")
        return starting_bid
