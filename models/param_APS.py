# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ParamAPS(models.Model):

    _name = 'ecole.aps'

    name = fields.Char(string='Name', copy=False)
    ref_service = fields.Char(string='Service reference')
    zone_code_ids = fields.Many2many(string='List of zone codes', comodel_name='ecole.zone.code')
