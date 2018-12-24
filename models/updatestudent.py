# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from school import *


class StudentUpdate(models.Model):
    _name = 'ecole.student.update'

# Fonction qui permet de récupérer les élèves actifs
    def _get_default_students(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_ids'))

# Fonction qui permet de récupérer l'établissement actif
    def _get_default_school(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_id')).school_name_id.id

# Fonction qui permet de récupérer la période par défaut
    @api.multi
    def _get_period_year(self):
        domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
        period_id = self.env['ecole.partner.school.years'].search(domain, limit=1).id

        return period_id

# Fonction qui permet de récupérer le niveau actif +1
    @api.multi
    def _get_default_level(self):
        level_id = self.env['ecole.partner.school'].browse(self.env.context.get('active_id'))
        new_level = level_id.school_level_id.id

        return new_level + 1

    student_ids = fields.Many2many('ecole.partner.school', String="Students", default=_get_default_students)
    school_name_id = fields.Many2one(comodel_name="horanet.school.establishment",
                                     string="Establishments",
                                     default=_get_default_school)
    school_year_id = fields.Many2one(string='Period',
                                     ondelete='SET NULL',
                                     comodel_name="ecole.partner.school.years",
                                     default=_get_period_year)
    school_level_id = fields.Many2one(comodel_name="horanet.school.grade",
                                      string="Level", default=_get_default_level)
    school_lvl_id = fields.Many2one(comodel_name="horanet.school.grade", string="Level")
    # Pour code terminaux
    extracurricular_activity_id = fields.Many2one(comodel_name="ecole.aps", string="Extracurricular activity place")
    nursery_wednesday_afternoon_name_id = fields.Many2one(comodel_name="ecole.nursery.school", string="Afternoon place")

# Récupère le niveau scolaire en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_new_grade_id(self):
        if self.school_name_id:
            establishment = self.school_name_id.name.split()[-1]
            records = self.env['horanet.school.grade'].search([])
            for rec in records:
                if rec.name:
                    level = rec.name
                    if establishment in level:
                        self.school_lvl_id = rec.id
                        break

# Récupère le lieu APS en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_new_aps_id(self):
        if self.school_name_id:
            records_aps_id = self.env['ecole.aps'].search([])
            for record in records_aps_id:
                if record.name:
                    aps_id = record.name.split()[-1]
                    if aps_id in self.school_name_id.name:
                        self.extracurricular_activity_id = record.id
                        break

# Récupère le lieu garderie après midi en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_new_afternoon_wednesday_nursery_id(self):
        if self.school_name_id:
                records_nursery = self.env['ecole.nursery.school'].search([])
                for record in records_nursery:
                    if record.name:
                        place_nursery = record.name.split()[-1]
                        if place_nursery in self.school_name_id.name:
                            self.nursery_wednesday_afternoon_name_id = record.id + 2
                            break

# Fonction qui permet le passage de fin d'année scolaire
    def set_student_level(self):
        for record in self:
            if record.student_ids:
                for rec in record.student_ids:

                    # Permettra de récupérer les bonnes dates inscription scolaire et garderie
                    domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
                    records_years = self.env['ecole.partner.school.years'].search(domain, limit=1)

                    if rec.school_year_id.id+1 != self.school_year_id.id:
                        raise ValidationError("Erreur : Les périodes scolaires ne correspondent pas. Merci de corriger")

                    school_level = rec.school_level_id.name
                    if "CM2" in school_level:
                        raise ValidationError("Erreur : Vous ne pouvez pas faire de passage de fin d'année "
                                              "pour les classe de CM2")

                    # establishment_name = self.school_name_id.name.split()[-1]
                    # if establishment_name not in self.school_level_id.name:
                    #     raise ValidationError("Erreur : Problème entre niveau et établissement. Merci de modifier")

                    # Récupère les valeurs des champs de la table ecole.partner.school
                    partner = rec.partner_id.id

                    # Récupère les valeurs de l'inscription - APS
                    extracurricular_activity = rec.extracurricular_activity
                    extracurricular_activity_id = self.extracurricular_activity_id.id

                    # Récupère les valeurs pour inscription par défaut - Garderie mercredi après-midi
                    nursery_wednesday_evening = rec.nursery_wednesday_evening
                    if nursery_wednesday_evening:
                        nursery_evening_days_value = 4
                    else:
                        nursery_evening_days_value = 0
                    nursery_wednesday_afternoon_name_id = self.nursery_wednesday_afternoon_name_id.id

                    # Récupère les valeurs des champs de la table ecole.student.update
                    new_year = self.school_year_id.id
                    new_level = self.school_level_id.id
                    new_school = self.school_name_id.id

                    # if new_school:
                    #     if nursery_wednesday_evening:
                    #         records_nursery = self.env['ecole.nursery.school'].search([])
                    #         for record_nursery in records_nursery:
                    #             if record_nursery.name:
                    #                 place_nursery = record_nursery.name.split()[-1]
                    #                 if place_nursery in self.school_name_id.name:
                    #                     nursery_wednesday_afternoon_name_id = record_nursery.id + 2
                    #                     break
                    #     if extracurricular_activity:
                    #         records_aps_id = self.env['ecole.aps'].search([])
                    #         for record_aps_id in records_aps_id:
                    #             if record_aps_id.name:
                    #                 aps_id = record_aps_id.name.split()[-1]
                    #                 if aps_id in self.school_name_id.name:
                    #                     extracurricular_activity_id = record_aps_id.id
                    #                     break

                    new_begin_date_id = records_years.year_begin_date
                    new_end_date_id = records_years.year_end_date

                    # Préparation du dictionnaire de valeurs
                    vals = {'partner_id': partner,
                            'extracurricular_activity': extracurricular_activity,
                            'extracurricular_activity_id': extracurricular_activity_id,
                            'school_year_id': new_year,
                            'school_registration': new_begin_date_id,
                            'school_end_date': new_end_date_id,
                            'school_name_id': new_school,
                            'school_level_id': new_level,
                            'nursery_wednesday_evening': nursery_wednesday_evening,
                            'nursery_evening_days_value': nursery_evening_days_value,
                            'nursery_wednesday_afternoon_name_id': nursery_wednesday_afternoon_name_id
                            }

                    rec.create(vals)

            # Retourne le popup de validation
            return {
                'name': 'Validation',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ecole.student.update',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new'
            }
