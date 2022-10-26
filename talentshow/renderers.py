from django.forms.widgets import DateInput, DateTimeInput, TimeInput

from dal.autocomplete import ModelSelect2
from django_addanother.widgets import AddAnotherWidgetWrapper

from django_bootstrap5 import renderers

class FieldRenderer(renderers.FieldRenderer):
    def add_class_attrs(self, widget=None):
        super().add_class_attrs(widget=widget)
        if widget is None:
            widget = self.widget

        if self.field.field.disabled:
            widget.attrs['class'] = 'form-control-plaintext'

    def add_date_attrs(self, widget=None):
        if not isinstance(widget, DateInput):
            return
        if widget is None:
            widget = self.widget
        widget.attrs["data-datetimepicker"] = widget.attrs.get(
            "data-datetimepicker", "date"
        )

    def add_datetime_attrs(self, widget=None):
        if not isinstance(widget, DateTimeInput):
            return
        if widget is None:
            widget = self.widget
        widget.attrs["data-datetimepicker"] = widget.attrs.get(
            "data-datetimepicker", "datetime"
        )

    def add_time_attrs(self, widget=None):
        if not isinstance(widget, TimeInput):
            return
        if widget is None:
            widget = self.widget
        widget.attrs["data-datetimepicker"] = widget.attrs.get(
            "data-datetimepicker", "time"
        )

    def fix_for_autocomplete(self, widget=None):
        if isinstance(widget, AddAnotherWidgetWrapper):
            widget = widget.widget

        if not isinstance(widget, ModelSelect2):
            return
        if widget is None:
            widget = self.widget
        widget.attrs["data-placeholder"] = widget.attrs.get(
            "placeholder", self.field.label
        )

    def add_widget_attrs(self):
        super().add_widget_attrs()
        if self.is_multi_widget:
            widgets = self.widget.widgets
        else:
            widgets = [self.widget]
        for widget in widgets:
            self.add_date_attrs(widget)
            self.add_datetime_attrs(widget)
            self.add_time_attrs(widget)
            self.fix_for_autocomplete(widget)


class FormRenderer(renderers.FormRenderer):
    def render_errors(self, type="non_fields"):
        return super().render_errors(type=type)