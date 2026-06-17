from django import forms
from django.core.validators import FileExtensionValidator
from .models import FormSubmission

ALLOWED_EXTENSIONS = ['pdf','doc','docx','xls','xlsx','ppt','pptx','jpg','jpeg','png']
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

class SubmissionForm(forms.ModelForm):
    attachment = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
    )

    class Meta:
        model = FormSubmission
        fields = ['title', 'form_type', 'description', 'attachment']

        def clean_attachment(self):
            file = self.clean_data.get('attachment')
            if file and file.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File too large.Maximum size is 10MB')
            return file