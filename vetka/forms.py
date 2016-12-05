from flask_wtf import FlaskForm
import wtforms
# from wtforms import StringField, BooleanField, TextAreaField, SelectField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from vetka import models


class MultiCheckboxField(wtforms.SelectMultipleField):
    widget = wtforms.widgets.ListWidget(prefix_label=False)
    option_widget = wtforms.widgets.CheckboxInput()
    pass


class AddGoodForm(FlaskForm):
    product = wtforms.StringField('product', validators=[DataRequired()])
    name = wtforms.StringField('name')
    name_en = wtforms.StringField('name_en', validators=[DataRequired()])
    description = wtforms.TextAreaField('description', validators=[DataRequired()])
    image = wtforms.StringField('image', validators=[DataRequired()])
    category = wtforms.SelectField('category', coerce=int)
    price = wtforms.IntegerField('price', validators=[DataRequired(), NumberRange(0, 1000)])
    priority = wtforms.RadioField('priority', coerce=int, choices=[(3, 'высокий'), (2, 'средний'), (1, 'низкий')],
                                  default=2)
    tags = MultiCheckboxField('tags', coerce=int)

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

        self.category.choices = [(cat.id, cat.name) for cat in models.Category.query.all() if cat.primary]
        self.tags.choices = [(tag.id, tag.name) for tag in models.Category.query.all() if not tag.primary]

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if self.__class__.__name__ == 'AddGoodForm':
            existing = models.Good.query.filter(models.Good.name_en == self.name_en.data).first()
            if existing is not None:
                self.name_en.errors.append('Good ' + existing.name_en + ' already exists')
                return False
        return True


class EditGoodForm(AddGoodForm):
    id = wtforms.HiddenField('id', validators=[DataRequired()])

    def validate(self):
        if not AddGoodForm.validate(self):
            return False
        return True


class AddTagForm(FlaskForm):
    name = wtforms.StringField('name', validators=[DataRequired()])
    name_en = wtforms.StringField('name_en', validators=[DataRequired()])
    description = wtforms.TextAreaField('description')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if self.__class__.__name__ == 'AddTagForm':
            existing = models.Category.query.filter(models.Category.name_en == self.name_en.data).first()
            if existing is not None:
                self.name_en.errors.append('Tag ' + existing.name_en + ' already exists')
                return False
        return True


class EditTagForm(AddTagForm):
    id = wtforms.HiddenField('id', validators=[DataRequired()])

    def validate(self):
        if not AddTagForm.validate(self):
            return False
        return True
