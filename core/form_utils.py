# -*- coding: utf-8 -*-

attrs_formcontrol = {'class': 'form-control'}
attrs_checkboxcontrol = {'class': 'pull-left checkbox-control'}
attrs_floatcontrol = {'class': 'form-control price-control', 'step': '0.01'}
attrs_numbercontrol = {'class': 'form-control', 'step': '1', 'min': '1'}
attrs_selectcontrol = {'class': 'select-with-search'}
attrs_editor = {'class': 'form-control'}
# attrs_single_date_picker = {'class':'form-control daterange-single'}
attrs_single_date_picker = {
    'class': 'form-control jq-datepicker-icon', "placeHolder": "MM/DD/YYYY"}
attrs_single_time_picker = {
    'class': 'form-control timepicker-icon', "placeHolder": "H:m"}
attrs_datetime_picker = {'class': 'form-control anytime-both'}
attrs_file_picker = {'data-clear-btn': 'true', 'class': 'file-styled'}
attrs_multiple_file_picker = {'data-clear-btn': 'true', 'class': 'file-input'}
attrs_is_active = {'data-size': 'mini', 'data-on-text': 'On', 'data-off-text': 'Off', 'class': 'switch',
                   'data-on-color': 'success'}


def applyClassConfig2FormControl(form):
    for field_name, field in form.fields.items():
        html_type = field.widget.__class__.__name__
        # print field_name ,field.__class__.__name__ , ':', html_type

        if html_type == "Textarea":
            field.widget.attrs = attrs_editor.copy()
        elif html_type == "Select":
            field.widget.attrs = attrs_selectcontrol.copy()
        elif html_type == "DateInput":
            field.widget.attrs = attrs_single_date_picker.copy()
        elif html_type == "TimeInput":
            field.widget.attrs = attrs_single_time_picker.copy()
        elif html_type == "CheckboxInput":
            field.widget.attrs = attrs_checkboxcontrol.copy()

        elif html_type == "DateTimeInput":
            field.widget.attrs = attrs_datetime_picker.copy()

        elif html_type == "NumberInput":
            if field.__class__.__name__ == "FloatField" or field.__class__.__name__ == "DecimalField":  # special edit for float
                field.widget.attrs = attrs_floatcontrol.copy()

            else:
                field.widget.attrs = attrs_numbercontrol.copy()
                #          aria-required="true" type="email" aria-invalid="true"
        elif html_type == "CustomClearableFileInputWidget":
            field.widget.attrs = attrs_file_picker.copy()

        elif html_type == "ClearableFileInput":
            field.widget.attrs = attrs_multiple_file_picker.copy()
        else:
            field.widget.attrs = attrs_formcontrol.copy()

        if field_name == 'is_active':
            field.widget.attrs = attrs_is_active.copy()
