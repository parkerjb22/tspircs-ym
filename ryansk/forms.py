from wtforms import Form, StringField, FileField
from wtforms.validators import DataRequired

class UploadForm(Form):
    url = StringField('URL:', validators=[DataRequired()])
    name = StringField('New name (optional)')
    file = FileField('File:')