# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SchoolEstablishmentWebServices(models.Model):

    _inherit = 'horanet.school.establishment'

    id_establishment = fields.Char(string='idEtablissement')

    establishment_wording = fields.Char(string='Wording')
    establishment_address = fields.Char(string='Address')
    establishment_cp = fields.Char(string='Postal code')
    establishment_city = fields.Char(string='City')
    establishment_phone = fields.Char(string='Phone')
    establishment_fax = fields.Char(string='Fax')
    establishment_mail = fields.Char(string='Mail address')
    establishment_manager = fields.Char(string='Manager')

    city_picture = fields.Binary(string="City picture")
    city_address_information = fields.Char(string='City address information')
    city_contact_information = fields.Char(string='City contact information')
    connected_person = fields.Char(string='Connected person')
    signature_connected_person = fields.Binary(string="Signature connected person")

    school_service_address = fields.Char(string='School service address')
    school_service_phone = fields.Char(string='Phone')
    school_service_fax = fields.Char(string='Fax')
    school_service_mail = fields.Char(string='Mail address')

    ref_service = fields.Char(string='Service reference')
    zone_code_ids = fields.Many2many(string='List of zone codes', comodel_name='ecole.zone.code')



