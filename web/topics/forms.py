from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Topic, Comment


class TopicCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title')
    body = forms.CharField(label='Body', required=False, widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))
    url = forms.CharField(label='Url', required=False)

    def is_valid(self):
        valid = super(TopicCreateForm, self).is_valid()

        if not valid:
            return valid

        if not self.cleaned_data['body'] and not self.cleaned_data['url']:
            self._errors['body'] = 'You need to fill body or url field.'
            self._errors['url'] = 'You need to fill body or url field.'
            return False

        if self.cleaned_data['url'] and not self.cleaned_data['body']:
            url_validate = URLValidator(schemes=['http', 'https'])

            try:
                url_validate(self.cleaned_data['url'])
            except ValidationError:
                self._errors['url'] = 'Please enter a valid url.'
                return False

        return True

    class Meta:
        model = Topic
        fields = ['title', 'body', 'url']


class CommentCreateForm(forms.ModelForm):
    body = forms.CharField(label='Body', widget=forms.TextInput)

    def is_valid(self):
        valid = super(CommentCreateForm, self).is_valid()

        if not valid:
            return valid

        topic = Topic.objects.get(pk=self.data['topic_id'])

        if not topic:
            self._errors['body'] = 'There is an error!'
            return False

        return True

    class Meta:
        model = Comment
        fields = ['body']
