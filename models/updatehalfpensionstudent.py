# -*- coding: utf-8 -*-
from pygments.lexer import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentUpdateHalfpension(models.Model):

    _name = 'ecole.halfpension.update'

    # Fonction qui permet de récupérer les élèves actifs
    def _get_default_students(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_ids'))

    # Fonction qui permet de récupérer la période par défaut
    @api.multi
    def _get_period_year(self):
        domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
        period_id = self.env['ecole.partner.school.years'].search(domain, limit=1).id

        return period_id

    # Fonction qui permet de récupérer l'établissement de restauration scolaire actif
    def _get_default_halfpension_id_school(self):
        return self.env['ecole.halfpension.school'].search([], limit=1).id

    # Fonction qui permet de récupérer le début d'année scolaire
    def _get_begin_date(self):
        domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
        begin_date_id = self.env['ecole.partner.school.years'].search(domain, limit=1).year_begin_date

        return begin_date_id

    # Fonction qui récupère la date de fin d'année scolaire
    def _get_end_date(self):
        domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
        end_date_id = self.env['ecole.partner.school.years'].search(domain, limit=1).year_end_date

        return end_date_id

    student_ids = fields.Many2many('ecole.partner.school',
                                   string="Students",
                                   default=_get_default_students)

    school_year_id = fields.Many2one(string='Period',
                                     ondelete='SET NULL',
                                     comodel_name="ecole.partner.school.years",
                                     default=_get_period_year)

    half_pension = fields.Boolean(string="Registered", default=True)

    half_pension_id = fields.Many2one(string='Place',
                                      comodel_name="ecole.halfpension.school",
                                      default=_get_default_halfpension_id_school)

    begin_date = fields.Date(string='Start', default=_get_begin_date)
    end_date = fields.Date(string='End', default=_get_end_date)

# Fonction qui permet le passage de fin d'année scolaire (restauration scolaire)
    def set_student_halfpension(self):
        for record in self:
            if record.student_ids:
                for rec in record.student_ids:
                    res_halfpension_old = rec.search([('id', '<', rec.id), ('partner_id', '=', rec.partner_id.id)],
                                                     limit=1, order='id desc')

                    new_half_pension_responsible_partner = res_halfpension_old.half_pension_responsible_partner.id
                    new_half_pension_status = res_halfpension_old.half_pension_status
                    new_half_pension_days_value = res_halfpension_old.half_pension_days_value
                    new_half_pension_allergy = res_halfpension_old.half_pension_allergy
                    new_half_pension_without_pork = res_halfpension_old.half_pension_without_pork
                    new_half_pension_without_meat = res_halfpension_old.half_pension_without_meat
                    new_half_pension_text = res_halfpension_old.half_pension_text

                    if rec.school_year_id != self.school_year_id:
                        raise ValidationError("Erreur : Incohérence au niveau de la période scolaire")

                    # Récupère les valeurs des champs de la table ecole.halfpension.update
                    new_year = self.school_year_id.id
                    new_half_pension = self.half_pension
                    new_half_pension_id = self.half_pension_id.id
                    new_half_pension_begin_date = self.begin_date
                    new_half_pension_end_date = self.end_date

                    # Préparation du dictionnaire de valeurs
                    vals = {'school_year_id': new_year,
                            'half_pension': new_half_pension,
                            'half_pension_id': new_half_pension_id,
                            'half_pension_begin_date': new_half_pension_begin_date,
                            'half_pension_end_date': new_half_pension_end_date,
                            'half_pension_responsible_partner': new_half_pension_responsible_partner,
                            'half_pension_status': new_half_pension_status,
                            'half_pension_days_value': new_half_pension_days_value,
                            'half_pension_allergy': new_half_pension_allergy,
                            'half_pension_without_pork': new_half_pension_without_pork,
                            'half_pension_without_meat': new_half_pension_without_meat,
                            'half_pension_text': new_half_pension_text
                            }

                    rec.write(vals)

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
