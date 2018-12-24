# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ParamZoneCode(models.Model):

    _name = 'ecole.zone.code'
    _rec_name = "zone_code"

    name = fields.Char(string='Name', copy=False)
    zone_code = fields.Char(string='Zone Code')
