# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime


class ResPartner(models.Model):

    _inherit = 'res.partner'

    scholarship_ids = fields.One2many(string='School card', comodel_name='ecole.partner.school',
                                      inverse_name='partner_id')
    difference_age = fields.Boolean(string='Age', compute="_date_now", store=False)
    compta_code = fields.Char(string='Compta code')
    # foyer_code_compta_ids = fields.One2many(string="Compta code",
    #                                         comodel_name='horanet.relation.foyer',
    #                                         inverse_name='foyer_id')

    # endregion


# Calcul de l'age pour afficher l'onglet scolaire sur la fiche d'un citoyen
    @api.one
    def _date_now(self):
        if self.birthdate_date:
            birth = fields.Date.from_string(self.birthdate_date)
            date_j = datetime.datetime.today()
            if ((date_j.year - birth.year) < 12) and ((date_j.year - birth.year) > 1):
                self.difference_age = True
        else:
            self.difference_age = True
