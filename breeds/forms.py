from django import forms
from .models import Breed


class BreedForm(forms.ModelForm):
    class Meta:
        model = Breed

        # ✅ INCLUDE ALL MODEL FIELDS USED BY UI CARDS
        fields = [
            'name',
            'category',
            'thumbnail',
            'description',
            'origin_location',

            # Production metrics
            'milk_yield',
            'milk_fat',
            'daily_yield',

            # Appearance & traits
            'color_description',
            'traits',

            # Media
            'video_link',

            # System
            'is_active',
        ]

        labels = {
            'name': 'Breed Name',
            'category': 'Category',
            'thumbnail': 'Thumbnail Image',
            'description': 'Description',
            'origin_location': 'Origin Location',
            'milk_yield': 'Milk Yield',
            'milk_fat': 'Milk Fat (%)',
            'daily_yield': 'Daily Yield',
            'color_description': 'Color Description',
            'traits': 'Key Traits',
            'video_link': 'Reference Video',
            'is_active': 'Active Status',
        }

        help_texts = {
            'thumbnail': 'Upload a representative image for this breed',
            'milk_yield': 'Example: 15–20 L/day',
            'milk_fat': 'Example: 4–6%',
            'daily_yield': 'Optional display value',
            'traits': 'Comma separated values (e.g. Heat tolerant, Disease resistant)',
            'video_link': 'Optional YouTube or external reference link',
        }

        widgets = {
            # ================= BASIC =================
            'name': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Breed name'
            }),

            'category': forms.Select(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400'
            }),

            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'hidden'  # custom upload UI
            }),

            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Detailed breed description'
            }),

            'origin_location': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Origin location'
            }),

            # ================= METRICS =================
            'milk_yield': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'e.g., 15–20 L/day'
            }),

            'milk_fat': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'e.g., 4–6%'
            }),

            'daily_yield': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Optional display value'
            }),

            # ================= APPEARANCE =================
            'color_description': forms.TextInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'e.g., Black & White, Brown, Fawn'
            }),

            'traits': forms.Textarea(attrs={
                'rows': 3,
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Heat tolerant, Disease resistant, High yield'
            }),

            # ================= MEDIA =================
            'video_link': forms.URLInput(attrs={
                'class': 'rounded-xl border-gray-200 w-full px-4 py-3 focus:ring-2 focus:ring-purple-400 focus:border-purple-400',
                'placeholder': 'Optional reference video link'
            }),

            # ================= SYSTEM =================
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-gray-300 text-purple-600 focus:ring-purple-400'
            }),
        }

    # ✅ FIXED: WORKS FOR ADD + EDIT
    def clean_name(self):
        """
        Prevent duplicate breed names (case-insensitive),
        but allow same name when editing current object.
        """
        name = self.cleaned_data.get('name')
        qs = Breed.objects.filter(name__iexact=name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("A breed with this name already exists.")

        return name
