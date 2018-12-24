# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError
from school import *


class StudentUpdate(models.Model):
    _name = 'ecole.gantt.planning'

# Fonction qui permet de récupérer les élèves actifs
    def _get_default_students_for_gantt(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_ids'))

# Fonction qui permet de récupérer l'établissement actif
    def _get_default_school_for_gantt(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_id')).school_name_id.id

# Fonction qui permet de récupérer le niveau actif +1
    @api.multi
    def _get_default_level_for_gantt(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_id')).school_level_id.id

    student_ids = fields.Many2many('ecole.partner.school', String="Students", default=_get_default_students_for_gantt)
    school_name_id = fields.Many2one(comodel_name="horanet.school.establishment",
                                     string="Establishments",
                                     default=_get_default_school_for_gantt,
                                     readonly=True)
    school_level_id = fields.Many2one(comodel_name="horanet.school.grade",
                                      string="Level",
                                      default=_get_default_level_for_gantt,
                                      readonly=True)
    begin_date = fields.Date(string='Start', copy=False, default=datetime.datetime.today())
    end_date = fields.Date(string='End', copy=False)
    date_start = fields.Datetime('Start Date', copy=False, index=True, readonly=True)
    date_finished = fields.Datetime('End Date', copy=False, index=True, readonly=True)

    @api.multi
    def set_student_planning(self):
        # Retourne le rapport pdf
        return {
            'name': 'Rapport planning',
            'type': 'ir.actions.report.xml',
            'report_name': 'ecole.report_planning_halfpension'

        }

# Permet de proposer automatiquement des dates (sur 1 mois)
    @api.onchange('begin_date')
    def end_date_default(self):
        if self.begin_date:
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            begin_date = datetime.strptime(self.begin_date, "%Y-%m-%d")
            end_date = (begin_date + relativedelta(months=+1)).date()
            self.end_date = end_date

# # Permet de vérifier que ce soit bien la même classe
#     @api.onchange('school_level_id')
#     def verify_level(self):
#         for rec in self:
#             if rec.school_level_id.id != self.school_level_id.id:
#                 raise ValidationError("Erreur : Les niveaux scolaires ne correspondent pas. Merci de corriger")

