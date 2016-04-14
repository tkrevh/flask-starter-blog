from flask_security.forms import ConfirmRegisterForm
from wtforms import TextField
from wtforms.validators import Required
        
class ExtendedRegisterForm(ConfirmRegisterForm):
    name = TextField('Name', [Required()])
