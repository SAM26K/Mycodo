# -*- coding: utf-8 -*-
#
# forms_input.py - Input Flask Forms
#
import logging

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms import widgets
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput

from mycodo.config_translations import TOOLTIPS_SETTINGS
from mycodo.mycodo_flask.utils.utils_general import generate_form_input_list
from mycodo.utils.inputs import parse_input_information

logger = logging.getLogger("mycodo.forms_input")


class DataBase(FlaskForm):
    reorder_type = StringField('Reorder Type', widget=widgets.HiddenInput())
    list_visible_elements = SelectMultipleField('New Order')
    reorder = SubmitField(
        TOOLTIPS_SETTINGS['save_order']['title'])


class InputAdd(FlaskForm):
    choices_inputs = []
    dict_inputs = parse_input_information()
    list_inputs_sorted = generate_form_input_list(dict_inputs)

    for each_input in list_inputs_sorted:
        if 'interfaces' not in dict_inputs[each_input]:
            choices_inputs.append(
                ('{inp},'.format(inp=each_input),
                 '{manuf}: {name}: {meas}'.format(
                     manuf=dict_inputs[each_input]['input_manufacturer'],
                     name=dict_inputs[each_input]['input_name'],
                     meas=dict_inputs[each_input]['measurements_name'])))
        else:
            for each_interface in dict_inputs[each_input]['interfaces']:
                choices_inputs.append(
                    ('{inp},{int}'.format(inp=each_input, int=each_interface),
                     '{manuf}: {name}: {meas} ({int})'.format(
                         manuf=dict_inputs[each_input]['input_manufacturer'],
                         name=dict_inputs[each_input]['input_name'],
                         meas=dict_inputs[each_input]['measurements_name'],
                         int=each_interface)))

    input_type = SelectField(
        choices=choices_inputs,
        validators=[DataRequired()]
    )
    input_add = SubmitField(
        TOOLTIPS_SETTINGS['add']['title'])


class InputMod(FlaskForm):
    input_id = StringField('Input ID', widget=widgets.HiddenInput())
    input_measurement_id = StringField(widget=widgets.HiddenInput())
    name = StringField(
        TOOLTIPS_SETTINGS['name']['title'],
        validators=[DataRequired()]
    )
    period = DecimalField(
        TOOLTIPS_SETTINGS['period']['title'],
        validators=[DataRequired(),
                    validators.NumberRange(
                        min=5.0,
                        max=86400.0
        )],
        widget=NumberInput(step='any')
    )
    location = StringField(lazy_gettext('Location'))
    ftdi_location = StringField(
        TOOLTIPS_SETTINGS['ftdi_location']['title'])
    uart_location = StringField(
        TOOLTIPS_SETTINGS['uart_location']['title'])
    i2c_location = StringField(
        TOOLTIPS_SETTINGS['i2c_location']['title'])
    gpio_location = IntegerField(
        TOOLTIPS_SETTINGS['gpio_location']['title'])

    i2c_bus = IntegerField(
        TOOLTIPS_SETTINGS['i2c_bus']['title'], widget=NumberInput())
    baud_rate = IntegerField(
        TOOLTIPS_SETTINGS['baud_rate']['title'], widget=NumberInput())
    power_output_id = StringField(
        lazy_gettext('Power Output'))  # For powering input
    calibrate_sensor_measure = StringField(
        lazy_gettext('Calibration Measurement'))
    resolution = IntegerField(
        TOOLTIPS_SETTINGS['resolution']['title'], widget=NumberInput())
    resolution_2 = IntegerField(
        TOOLTIPS_SETTINGS['resolution']['title'], widget=NumberInput())
    sensitivity = IntegerField(
        TOOLTIPS_SETTINGS['sensitivity']['title'], widget=NumberInput())

    measurements_enabled = SelectMultipleField(
        TOOLTIPS_SETTINGS['measurements_enabled']['title'])

    # Server options
    host = StringField(
        TOOLTIPS_SETTINGS['host']['title'])
    port = IntegerField(
        TOOLTIPS_SETTINGS['port']['title'], widget=NumberInput())
    times_check = IntegerField(
        TOOLTIPS_SETTINGS['times_check']['title'], widget=NumberInput())
    deadline = IntegerField(
        TOOLTIPS_SETTINGS['deadline']['title'], widget=NumberInput())

    # Linux Command
    cmd_command = StringField(
        TOOLTIPS_SETTINGS['cmd_command']['title'])

    # MAX chip options
    thermocouple_type = StringField(
        TOOLTIPS_SETTINGS['thermocouple_type']['title'])
    ref_ohm = IntegerField(
        TOOLTIPS_SETTINGS['ref_ohm']['title'], widget=NumberInput())

    # SPI Communication
    pin_clock = IntegerField(
        TOOLTIPS_SETTINGS['pin_clock']['title'], widget=NumberInput())
    pin_cs = IntegerField(
        TOOLTIPS_SETTINGS['pin_cs']['title'], widget=NumberInput())
    pin_mosi = IntegerField(
        TOOLTIPS_SETTINGS['pin_mosi']['title'], widget=NumberInput())
    pin_miso = IntegerField(
        TOOLTIPS_SETTINGS['pin_miso']['title'], widget=NumberInput())

    # Bluetooth Communication
    bt_adapter = StringField(lazy_gettext('BT Adapter (hci[X])'))

    # ADC
    adc_gain = IntegerField(
        TOOLTIPS_SETTINGS['adc_gain']['title'], widget=NumberInput())
    adc_resolution = IntegerField(
        TOOLTIPS_SETTINGS['adc_resolution']['title'], widget=NumberInput())
    adc_sample_speed = StringField(
        TOOLTIPS_SETTINGS['adc_sample_speed']['title'])

    switch_edge = StringField(lazy_gettext('Edge'))
    switch_bouncetime = IntegerField(
        lazy_gettext('Bounce Time (ms)'), widget=NumberInput())
    switch_reset_period = IntegerField(
        lazy_gettext('Reset Period'), widget=NumberInput())

    # Pre-Output
    pre_output_id = StringField(
        TOOLTIPS_SETTINGS['pre_output_id']['title'])
    pre_output_duration = DecimalField(
        TOOLTIPS_SETTINGS['pre_output_duration']['title'],
        validators=[validators.NumberRange(
            min=0,
            max=86400
        )],
        widget=NumberInput(step='any')
    )
    pre_output_during_measure = BooleanField(
        TOOLTIPS_SETTINGS['pre_output_during_measure']['title'])

    # RPM/Signal
    weighting = DecimalField(
        TOOLTIPS_SETTINGS['weighting']['title'],
        widget=NumberInput(step='any'))
    rpm_pulses_per_rev = DecimalField(
        TOOLTIPS_SETTINGS['rpm_pulses_per_rev']['title'],
        widget=NumberInput(step='any'))
    sample_time = DecimalField(
        TOOLTIPS_SETTINGS['sample_time']['title'],
        widget=NumberInput(step='any'))

    # SHT options
    sht_voltage = StringField(
        TOOLTIPS_SETTINGS['sht_voltage']['title'])

    input_mod = SubmitField(
        TOOLTIPS_SETTINGS['save']['title'])
    input_delete = SubmitField(
        TOOLTIPS_SETTINGS['delete']['title'])
    input_acquire_measurements = SubmitField(lazy_gettext('Acquire Measurements Now'))
    input_activate = SubmitField(
        TOOLTIPS_SETTINGS['activate']['title'])
    input_deactivate = SubmitField(
        TOOLTIPS_SETTINGS['deactivate']['title'])
    input_order_up = SubmitField(
        TOOLTIPS_SETTINGS['up']['title'])
    input_order_down = SubmitField(
        TOOLTIPS_SETTINGS['down']['title'])


class InputMeasurementMod(FlaskForm):
    input_id = StringField('Input ID', widget=widgets.HiddenInput())
    input_measurement_id = StringField(widget=widgets.HiddenInput())
    name = StringField(
        TOOLTIPS_SETTINGS['name']['title'], validators=[DataRequired()]
    )
    select_measurement_unit = StringField(
        TOOLTIPS_SETTINGS['select_measurement_unit']['title'])

    scale_from_min = DecimalField(
        TOOLTIPS_SETTINGS['scale_from_min']['title'],
        widget=NumberInput(step='any'))
    scale_from_max = DecimalField(
        TOOLTIPS_SETTINGS['scale_from_max']['title'],
        widget=NumberInput(step='any'))
    scale_to_min = DecimalField(
        TOOLTIPS_SETTINGS['scale_to_min']['title'],
        widget=NumberInput(step='any'))
    scale_to_max = DecimalField(
        TOOLTIPS_SETTINGS['scale_to_max']['title'],
        widget=NumberInput(step='any'))
    invert_scale = BooleanField(
        TOOLTIPS_SETTINGS['invert_scale']['title'])

    rescaled_measurement_unit = StringField(
        lazy_gettext('Rescaled Measurement'))
    convert_to_measurement_unit = StringField(
        TOOLTIPS_SETTINGS['convert_to_measurement_unit']['title'])

    input_measurement_mod = SubmitField(
        TOOLTIPS_SETTINGS['save']['title'])
