# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NurserySchool(models.Model):

    _name = 'ecole.nursery.school'

    name = fields.Char(string='Name', copy=False)
    code_Product = fields.Char(string='Product Code')
    code_CDG = fields.Char(string='Management Center')
    code_Catalog = fields.Char(string='Product catalogue')
    group_id = fields.Many2one(comodel_name="res.groups", string="Group")
    ref_service = fields.Char(string='Service reference')
    zone_code_ids = fields.Many2many(string='List of zone codes', comodel_name='ecole.zone.code')
