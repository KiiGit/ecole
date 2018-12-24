# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from functions import *
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class ResPartnerSchool(models.Model):

    _name = 'ecole.partner.school'
    _order = 'id desc'

    # Fonction qui permet de récupérer la période par défaut
    @api.multi
    def _get_period_year(self):
        domain = [('period_school_year', '=', False), ('default_school_year', '=', True)]
        period_id = self.env['ecole.partner.school.years'].search(domain, limit=1).id
        if period_id:
            return period_id

    # region Private attributes

    partner_id = fields.Many2one(string="Child", comodel_name="res.partner")

    school_year_id = fields.Many2one(string='Period',
                                     ondelete='SET NULL',
                                     comodel_name="ecole.partner.school.years",
                                     default=_get_period_year)
    school_year_id_rel = fields.Char(string='Period', store=False, compute='_compute_period_id')
    school_registration = fields.Date(string='Begin',
                                      copy=False)
    school_end_date = fields.Date(string='End',
                                  copy=False)

    extracurricular_activity = fields.Boolean(string='APS', copy=False)
    extracurricular_activity_id = fields.Many2one(comodel_name="ecole.aps", string="Extracurricular activity place")
    default_school_year = fields.Boolean(string='Current year',
                                         readonly="1",
                                         related='school_year_id.default_school_year',
                                         copy=False)  # Pour filtre
    period_school_year = fields.Boolean(string='Next year',
                                        readonly="1",
                                        related='school_year_id.period_school_year',
                                        copy=False)  # Pour filtre
    school_name_id = fields.Many2one(comodel_name="horanet.school.establishment", string="Establishment")
    school_level_id = fields.Many2one(comodel_name="horanet.school.grade",
                                      string="Level")
    school_lvl = fields.Many2one(comodel_name="horanet.school.grade", string="Level")

    half_pension_tree_view = fields.Boolean(string='Restauration', copy=False, store=False,
                                            compute='_retrieve_halfpension_for_tab')
    half_pension = fields.Boolean(string='Catering', copy=False)
    half_pension_unsubscribe = fields.Boolean(string='Closing contract', copy=False)
    half_pension_previous = fields.Boolean(string='previously registered', copy=False, store=True,
                                           compute='_retrieve_halfpension_previous')
    half_pension_begin_date = fields.Date(string='Start', copy=False)
    half_pension_end_date = fields.Date(string='End', copy=False)
    half_pension_id = fields.Many2one(comodel_name="ecole.halfpension.school", string="Place")
    half_pension_days_value = fields.Integer(string='Days value', copy=False, store=True)
    half_pension_monday = fields.Boolean(string='Monday', copy=False, store=False,
                                         compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_tuesday = fields.Boolean(string='Tuesday', copy=False, store=False,
                                          compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_wednesday = fields.Boolean(string='Wednesday', copy=True, readonly="1", store=False,
                                            compute='convert_dec_bin_halfpension')
    half_pension_thursday = fields.Boolean(string='Thursday', copy=True, store=False,
                                           compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_friday = fields.Boolean(string='Friday', copy=True, store=False,
                                         compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_occasional = fields.Boolean(string='Occasional registred', copy=False)
    half_pension_specification = fields.Boolean(string='Specifications', copy=False, store=False,
                                                compute='_retrieve_specification_for_view',
                                                groups="ecole.group_ecole_restauration_scolaire")
    half_pension_allergy = fields.Boolean(string='Allergies', copy=False)
    half_pension_text = fields.Text(string="Observations", copy=False,
                                    groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_pork = fields.Boolean(string='Without pork', copy=False,
                                               groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_meat = fields.Boolean(string='Without meat', copy=False,
                                               groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_bulletin = fields.Boolean(string='Without registration form', copy=False,
                                                   groups="ecole.group_ecole_restauration_scolaire")
    half_pension_responsible_partner = fields.Many2one(string="Paying agent",
                                                       comodel_name="res.partner",
                                                       domain="[('search_field_all_foyers_members', 'in', partner_id)]",
                                                       readonly=False)
    half_pension_status = fields.Char(string="Status", copy=False, store=True)

    nursery = fields.Boolean(string='Nursery', copy=False, store=False, compute='_retrieve_nursery_for_tab')
    nursery_morning_unsubscribe = fields.Boolean(string='Closing morning contract', copy=False)
    nursery_evening_unsubscribe = fields.Boolean(string='Closing evening contract', copy=False)
    nursery_morning = fields.Boolean(string='Nursery morning', copy=False)
    nursery_evening = fields.Boolean(string='Nursery evening', copy=False)
    nursery_begin_date = fields.Date(string='Start', copy=False)
    nursery_end_date = fields.Date(string='End', copy=False)
    nursery_name_id = fields.Many2one(comodel_name="ecole.nursery.school", string="Morning place")
    nursery_two_name_id = fields.Many2one(comodel_name="ecole.nursery.school", string="Evening place")
    nursery_wednesday_afternoon_name_id = fields.Many2one(comodel_name="ecole.nursery.school", string="Afternoon place")
    nursery_morning_days_value = fields.Integer(string='Days value', copy=False, store=True)
    nursery_monday_morning = fields.Boolean(string='Monday morning', copy=False, store=False,
                                            compute='convert_for_nursery_morning', readonly=False)
    nursery_tuesday_morning = fields.Boolean(string='Tuesday morning', copy=False, store=False,
                                             compute='convert_for_nursery_morning', readonly=False)
    nursery_wednesday_morning = fields.Boolean(string='Wednesday morning', copy=False, store=False,
                                               compute='convert_for_nursery_morning', readonly=False)
    nursery_thursday_morning = fields.Boolean(string='Thursday morning', copy=False, store=False,
                                              compute='convert_for_nursery_morning', readonly=False)
    nursery_friday_morning = fields.Boolean(string='Friday morning', copy=False, store=False,
                                            compute='convert_for_nursery_morning', readonly=False)
    nursery_evening_days_value = fields.Integer(string='Days value', copy=False, store=True)
    nursery_monday_evening = fields.Boolean(string='Monday evening', copy=False, store=False,
                                            compute='convert_for_nursery_evening', readonly=False)
    nursery_tuesday_evening = fields.Boolean(string='Tuesday evening', copy=False, store=False,
                                             compute='convert_for_nursery_evening', readonly=False)
    nursery_wednesday_evening = fields.Boolean(string='Wednesday afternoon', copy=False, store=False,
                                               compute='convert_for_nursery_evening', readonly=False)
    nursery_thursday_evening = fields.Boolean(string='Thursday evening', copy=False, store=False,
                                              compute='convert_for_nursery_evening', readonly=False)
    nursery_friday_evening = fields.Boolean(string='Friday evening', copy=False, store=False,
                                            compute='convert_for_nursery_evening', readonly=False)
    nursery_text = fields.Text(string="Observations", groups="ecole.group_ecole_garderie")
    nursery_responsible_partner = fields.Many2one(string="Paying agent",
                                                  comodel_name="res.partner",
                                                  domain="[('search_field_all_foyers_members', 'in', partner_id)]",
                                                  readonly=False)
    nursery_status_morning = fields.Char(string="Status", copy=False, store=True)
    nursery_status_evening = fields.Char(string="Status", copy=False, store=True)

    resp_civility1 = fields.Char(string="Civility", copy=False)
    resp_name1 = fields.Char(string="Name and First name", copy=False)
    resp_cp1 = fields.Char(string="Postal code", copy=False)
    resp_num1 = fields.Char(string="Number", copy=False)
    resp_address1 = fields.Char(string="Address", copy=False)
    resp_town1 = fields.Char(string="Town", copy=False)
    resp_phone1 = fields.Char(string="Phone", copy=False)
    resp_phonemobile1 = fields.Char(string="Mobile", copy=False)
    resp_filiation1 = fields.Char(string="Filiation", copy=False)

    resp_civility2 = fields.Char(string="Civility", copy=False)
    resp_name2 = fields.Char(string="Name and First name", copy=False)
    resp_cp2 = fields.Char(string="Postal code", copy=False)
    resp_num2 = fields.Char(string="Number", copy=False)
    resp_address2 = fields.Char(string="Address", copy=False)
    resp_town2 = fields.Char(string="Town", copy=False)
    resp_phone2 = fields.Char(string="Phone", copy=False)
    resp_phonemobile2 = fields.Char(string="Mobile", copy=False)
    resp_filiation2 = fields.Char(string="Filiation", copy=False)

    # endregion

# Récupère le titulaire responsable d'un partner par défaut
    @api.onchange('partner_id')
    def _get_responsible_foyer(self):
        if self.partner_id:
            actually_partner_id = self.partner_id.name
            if actually_partner_id:
                records_foyer_id = self.env['horanet.relation.foyer'].search([('partner_id', '=', actually_partner_id)])
                for rec_foyer in records_foyer_id:
                    if rec_foyer.foyer_id:
                        records_partner_id = self.env['horanet.relation.foyer'].search(
                            [('foyer_id', '=', rec_foyer.foyer_id.id), ('is_responsible', '=', True)])
                        for rec_partner in records_partner_id:
                            if rec_partner.partner_id:
                                self.half_pension_responsible_partner = rec_partner.partner_id.id
                                self.nursery_responsible_partner = rec_partner.partner_id.id

# Permet de récupérer les coordonnées du responsable - Garderie
    @api.onchange('nursery_morning', 'nursery_evening', 'nursery_responsible_partner')
    def retrieve_responsible_nursery(self):
        if self.nursery_morning or self.nursery_evening:
            if self.nursery_responsible_partner:
                self.resp_civility1 = self.nursery_responsible_partner.title.name
                self.resp_name1 = self.nursery_responsible_partner.name
                self.resp_cp1 = self.nursery_responsible_partner.zip_id.name
                self.resp_num1 = self.nursery_responsible_partner.street_number_id.name
                self.resp_address1 = self.nursery_responsible_partner.street_id.name
                self.resp_town1 = self.nursery_responsible_partner.city_id.name
                self.resp_phone1 = self.nursery_responsible_partner.phone
                self.resp_phonemobile1 = self.nursery_responsible_partner.mobile


# Fonction qui permet de décocher les jours d'inscription si le booléen "inscription occasionel" est coché
    @api.onchange('half_pension_occasional')
    def _days_registration_halfpension(self):
        if self.half_pension_occasional:
            self.half_pension_monday = False
            self.half_pension_tuesday = False
            self.half_pension_thursday = False
            self.half_pension_friday = False
        else:
            self.half_pension_monday = True
            self.half_pension_tuesday = True
            self.half_pension_thursday = True
            self.half_pension_friday = True

# Récupère la valeur des champs booléens garderie matin ou soir pour la visualiser dans l'onglet scolaire
    @api.depends('nursery_morning', 'nursery_evening', 'nursery_morning_unsubscribe', 'nursery_evening_unsubscribe')
    def _retrieve_nursery_for_tab(self):
        for rec in self:
            if rec.nursery_morning or rec.nursery_evening:
                rec.nursery = True
            if rec.nursery_morning_unsubscribe and rec.nursery_evening_unsubscribe:
                rec.nursery = False

# Récupère la valeur des champs booléens half_pension et half_pension_unsubscribe visualiser dans l'onglet scolaire
    @api.depends('half_pension', 'half_pension_unsubscribe')
    def _retrieve_halfpension_for_tab(self):
        for rec in self:
            if rec.half_pension:
                rec.half_pension_tree_view = True
            if rec.half_pension and rec.half_pension_unsubscribe:
                rec.half_pension_tree_view = False

# Récupère la valeur des champs booléens pour simplifier la vue liste des élèves - restauration scolaire
    @api.depends('half_pension_allergy',
                 'half_pension_without_pork',
                 'half_pension_without_meat',
                 'half_pension_allergy')
    def _retrieve_specification_for_view(self):
        for rec in self:
            if rec.half_pension_allergy or rec.half_pension_without_pork or rec.half_pension_without_meat \
                    or rec.half_pension_allergy:
                rec.half_pension_specification = True

# Récupère la valeur du champs booléen inscription de l'année précédente
    @api.depends('half_pension')
    def _retrieve_halfpension_previous(self):
        for record in self:
            res_halfpension = self.env['ecole.partner.school'].search([('id', '<', record.id),
                                                                       ('partner_id', '=', record.partner_id.id)],
                                                                      limit=1, order='id desc')
            if res_halfpension and not res_halfpension.half_pension_unsubscribe:
                record.half_pension_previous = res_halfpension.half_pension

# Récupère le niveau scolaire en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_grade_id(self):
        if self.school_name_id:
            # Récupère le dernier élément du name (horanet.school.establishment)
            establishment = self.school_name_id.name.split()[-1]
            records = self.env['horanet.school.grade'].search([])
            for rec in records:
                if rec.name:
                    level = rec.name
                    # Si ce que contient la variable establishment est dans la variable level
                    if establishment in level:
                        # Alors le champ school_level_id sera égale au premier champ dont la valeur trouvé est identique
                        self.school_level_id = rec.id
                        self.school_lvl = rec.id
                        break

# Récupère le lieu APS en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_aps_id(self):
        if self.school_name_id:
            records_aps_id = self.env['ecole.aps'].search([])
            self.extracurricular_activity = True
            if self.school_name_id.ref_service:
                if self.extracurricular_activity:
                    for record in records_aps_id:
                        if record.name:
                            aps_id = record.name.split()[-1]
                            if aps_id in self.school_name_id.name:
                                self.extracurricular_activity_id = record.id
                                break
            else:
                self.extracurricular_activity = False
        else:
            self.extracurricular_activity = False

# Récupère le lieu garderie après midi en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_afternoon_wednesday_nursery_id(self):
        if self.school_name_id:
            records_nursery = self.env['ecole.nursery.school'].search([])
            self.nursery_wednesday_evening = True
            if self.school_name_id.ref_service:
                if self.nursery_wednesday_evening:
                    for record in records_nursery:
                        if record.name:
                            place_nursery = record.name.split()[-1]
                            if place_nursery in self.school_name_id.name:
                                self.nursery_wednesday_afternoon_name_id = record.id+2
                                break
            else:
                self.nursery_wednesday_evening = False
        else:
            self.nursery_wednesday_evening = False

# Fonction qui récupère le lieu de restauration en fonction de l'établissement scolaire
    @api.onchange('half_pension')
    def retrieve_halfpension_place(self):
        if self.half_pension:
            records_halfpension = self.env['ecole.halfpension.school'].search([])
            for record in records_halfpension:
                if record.name:
                    place_halfpension = record.name.split()[-1]
                    if place_halfpension in self.school_name_id.name:
                        self.half_pension_id = record.id
                        break

# Fonction qui récupère le lieu de garderie en fonction de l'établissement scolaire
    @api.onchange('nursery_morning', 'nursery_evening')
    def retrieve_nursery_place(self):
        if self.nursery_morning or self.nursery_evening:
            records_nursery = self.env['ecole.nursery.school'].search([])
            for record in records_nursery:
                if record.name:
                    place_nursery = record.name.split()[-1]
                    if place_nursery in self.school_name_id.name:
                        self.nursery_name_id = record.id
                        self.nursery_two_name_id = record.id+1
                        break

# Fonction qui permet d'éviter des chevauchement de dates (inscriptions scolaires).
    @api.multi
    def no_duplicate_school_dates(self):
        for record in self:
            if record.school_registration or record.school_end_date:
                if record.school_registration > record.school_end_date:
                    raise ValidationError("Erreur : Problème dates. Merci de modifier")
                # Récupère les enregistrement actifs sauf l'actuel
                records = self.env['ecole.partner.school'].search([('id', '<', record.id),
                                                                   ('partner_id', '=', record.partner_id.id)])
                for rec in records:
                    if rec.school_year_id == record.school_year_id:
                        if rec.school_registration and rec.school_end_date:
                            if rec.school_name_id == self.school_name_id and rec.school_level_id == self.school_level_id:
                                if (rec.school_registration <= self.school_registration <= rec.school_end_date)\
                                        or (rec.school_registration <= self.school_end_date <= rec.school_end_date):
                                    raise ValidationError("Erreur : La plage de date en chevauche une autre. "
                                                          "Merci de modifier l'enregistrement précédent")
                            else:
                                end_date = self.school_registration
                                rec.school_end_date = fields.Date.from_string(end_date) + datetime.timedelta(-1)
                                break

# Fonction qui permet d'avoir une plage de dates compris dans la période scolaire
    @api.onchange('school_registration', 'school_end_date')
    def date_included_period(self):
        if self.school_year_id:
            begin_period_years = fields.Date.from_string(self.school_year_id.year_begin_date)
            end_period_years = fields.Date.from_string(self.school_year_id.year_end_date)
            begin_period = fields.Date.from_string(self.school_registration)
            end_period = fields.Date.from_string(self.school_end_date)
            if begin_period < begin_period_years or end_period > end_period_years:
                raise ValidationError("Erreur : Veuillez respecter la période scolaire qui doit être comprise "
                                      "entre le " + str(begin_period_years.strftime('%d-%m-%Y')) + " et "
                                      "le " + str(end_period_years.strftime('%d-%m-%Y')))

# Fonction qui permet d'avoir un visuel sur la période actuelle sur la fiche principale
    @api.depends('school_year_id')
    def _compute_period_id(self):
        for record in self:
            if record.school_year_id:
                record.school_year_id_rel = record.school_year_id.school_years

# Fonction relation entre dates années scolaire et dates des différents services
    @api.onchange('school_year_id')
    def _change_begin_date(self):
        if self.school_year_id:
            begin_date_id = self.school_year_id.year_begin_date
            begin_date = fields.Date.from_string(begin_date_id)
            date_j = datetime.date.today()
            end_date_id = self.school_year_id.year_end_date
            if begin_date > date_j:
                self.school_registration = begin_date_id
            else:
                self.school_registration = date_j
            self.school_end_date = end_date_id

# Fonction relation entre dates inscription scolaire et restauration scolaire
    @api.onchange('half_pension')
    def _change_dates_halfpension(self):
        if self.half_pension:
            if self.school_registration:
                self.half_pension_begin_date = self.school_registration
            if self.school_end_date:
                self.half_pension_end_date = self.school_end_date

# Fonction relation entre dates inscription scolaire et garderie
    @api.onchange('nursery_morning', 'nursery_evening')
    def _change_dates_nursery(self):
        if self.nursery_morning or self.nursery_evening:
            if self.school_registration:
                self.nursery_begin_date = self.school_registration
            if self.school_end_date:
                self.nursery_end_date = self.school_end_date

# Fonction qui modifie la valeur du booleen selon l'état du champ half_pension
    @api.onchange('half_pension')
    def _default_day_halfpension_value(self):
        if self.half_pension:
            self.half_pension_monday = self.half_pension
            self.half_pension_tuesday = self.half_pension
            self.half_pension_thursday = self.half_pension
            self.half_pension_friday = self.half_pension
        else:
            self.half_pension_monday = False
            self.half_pension_tuesday = False
            self.half_pension_thursday = False
            self.half_pension_friday = False

# Fonction qui modifie la valeur du booleen selon l'état du champ nursery_morning
    @api.onchange('nursery_morning')
    def default_day_nursery_morning_value(self):
        if self.nursery_morning:
            self.nursery_monday_morning = self.nursery_morning
            self.nursery_tuesday_morning = self.nursery_morning
            self.nursery_wednesday_morning = self.nursery_morning
            self.nursery_thursday_morning = self.nursery_morning
            self.nursery_friday_morning = self.nursery_morning
        else:
            self.nursery_monday_morning = False
            self.nursery_tuesday_morning = False
            self.nursery_wednesday_morning = False
            self.nursery_thursday_morning = False
            self.nursery_friday_morning = False

# Fonction qui modifie la valeur du booleen selon l'état du champ nursery_evening
    @api.onchange('nursery_evening')
    def default_day_nursery_evening_value(self):
        if self.nursery_evening:
            self.nursery_monday_evening = self.nursery_evening
            self.nursery_tuesday_evening = self.nursery_evening
            self.nursery_wednesday_evening = self.nursery_evening
            self.nursery_thursday_evening = self.nursery_evening
            self.nursery_friday_evening = self.nursery_evening
        else:
            self.nursery_monday_evening = False
            self.nursery_tuesday_evening = False
            # self.nursery_wednesday_evening = False
            self.nursery_thursday_evening = False
            self.nursery_friday_evening = False

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Garderie matin
    @api.onchange('nursery_morning', 'nursery_monday_morning', 'nursery_tuesday_morning', 'nursery_wednesday_morning',
                  'nursery_thursday_morning', 'nursery_friday_morning')
    def convert_bin_dec_nursery_morning(self):
        for record in self:
            if record.nursery_morning:
                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.nursery_monday_morning, record.nursery_tuesday_morning,
                                                     record.nursery_wednesday_morning, record.nursery_thursday_morning,
                                                     record.nursery_friday_morning)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.nursery_morning_days_value = total_decimal
            else:
                record.nursery_morning_days_value = 0

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Garderie soir
    @api.onchange('nursery_evening', 'nursery_monday_evening', 'nursery_tuesday_evening', 'nursery_wednesday_evening',
                  'nursery_thursday_evening', 'nursery_friday_evening')
    def convert_bin_dec_nursery_evening(self):
        for record in self:
            if record.nursery_evening:
                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.nursery_monday_evening, record.nursery_tuesday_evening,
                                                     record.nursery_wednesday_evening, record.nursery_thursday_evening,
                                                     record.nursery_friday_evening)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.nursery_evening_days_value = total_decimal
            else:
                if record.nursery_wednesday_evening:
                    record.nursery_evening_days_value = 4
                else:
                    record.nursery_evening_days_value = 0

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Restauration
    @api.onchange('half_pension', 'half_pension_monday', 'half_pension_tuesday', 'half_pension_wednesday',
                  'half_pension_thursday', 'half_pension_friday')
    def convert_bin_dec_halfpension(self):
        for record in self:
            if record.half_pension:
                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.half_pension_monday, record.half_pension_tuesday,
                                                     record.half_pension_wednesday, record.half_pension_thursday,
                                                     record.half_pension_friday)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.half_pension_days_value = total_decimal
            else:
                record.half_pension_days_value = 0

# Fonction qui permet de changer la status si l'enfant n'est plus inscrit - Restauration scolaire
    @api.onchange('half_pension', 'half_pension_unsubscribe')
    def change_status_half_pension(self):
        for record in self:
            if record.half_pension:
                record.half_pension_status = "2"
            else:
                record.half_pension_status = "3"
            if record.half_pension_unsubscribe and record.half_pension:
                record.half_pension_status = "3"

# Fonction qui permet de changer la status si l'enfant n'est plus inscrit - Garderie matin
    @api.onchange('nursery_morning', 'nursery_morning_unsubscribe')
    def change_status_nursery_morning(self):
        for record in self:
            if record.nursery_morning:
                record.nursery_status_morning = "2"
            else:
                record.nursery_status_morning = "3"
            if record.nursery_morning_unsubscribe and record.nursery_morning:
                record.nursery_status_morning = "3"

# Fonction qui permet de changer la status si l'enfant n'est plus inscrit - Garderie soir
    @api.onchange('nursery_evening', 'nursery_evening_unsubscribe')
    def change_status_nursery_evening(self):
        for record in self:
            if record.nursery_evening:
                record.nursery_status_evening = "2"
            else:
                record.nursery_status_evening = "3"
            if record.nursery_evening_unsubscribe and record.nursery_evening:
                record.nursery_status_evening = "3"

# Fonction qui permet d'avoir un visuel sur les jours d'inscription - Garderie matin
    @api.depends('nursery_morning_days_value')
    def convert_for_nursery_morning(self):
        for rec in self:
            if rec.nursery_morning_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.nursery_morning_days_value, 7)
                # rec.half_pension_days_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.nursery_monday_morning = True
                else:
                    rec.nursery_monday_morning = False
                if list_values[5] != '0':
                    rec.nursery_tuesday_morning = True
                else:
                    rec.nursery_tuesday_morning = False
                if list_values[4] != '0':
                    rec.nursery_wednesday_morning = True
                else:
                    rec.nursery_wednesday_morning = False
                if list_values[3] != '0':
                    rec.nursery_thursday_morning = True
                else:
                    rec.nursery_thursday_morning = False
                if list_values[2] != '0':
                    rec.nursery_friday_morning = True
                else:
                    rec.nursery_friday_morning = False

# Fonction qui permet d'avoir un visuel sur les jours d'inscription - Garderie soir
    @api.depends('nursery_evening_days_value')
    def convert_for_nursery_evening(self):
        for rec in self:
            if rec.nursery_evening_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.nursery_evening_days_value, 7)
                # rec.half_pension_days_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.nursery_monday_evening = True
                else:
                    rec.nursery_monday_evening = False
                if list_values[5] != '0':
                    rec.nursery_tuesday_evening = True
                else:
                    rec.nursery_tuesday_evening = False
                if list_values[4] != '0':
                    rec.nursery_wednesday_evening = True
                else:
                    rec.nursery_wednesday_evening = False
                if list_values[3] != '0':
                    rec.nursery_thursday_evening = True
                else:
                    rec.nursery_thursday_evening = False
                if list_values[2] != '0':
                    rec.nursery_friday_evening = True
                else:
                    rec.nursery_friday_evening = False

# Fonction qui permet d'avoir un visuel sur les jours d'inscription à la restauration scolaire
    @api.depends('half_pension_days_value')
    def convert_dec_bin_halfpension(self):
        for rec in self:
            if rec.half_pension_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.half_pension_days_value, 7)
                # rec.half_pension_days_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.half_pension_monday = True
                else:
                    rec.half_pension_monday = False
                if list_values[5] != '0':
                    rec.half_pension_tuesday = True
                else:
                    rec.half_pension_tuesday = False
                if list_values[4] != '0':
                    rec.half_pension_wednesday = True
                else:
                    rec.half_pension_wednesday = False
                if list_values[3] != '0':
                    rec.half_pension_thursday = True
                else:
                    rec.half_pension_thursday = False
                if list_values[2] != '0':
                    rec.half_pension_friday = True
                else:
                    rec.half_pension_friday = False

    # Fonction qui permet de synchroniser cantine et établissement scolaire avec SmartBambi
    @api.multi
    def smart_synchronization(self):
        for record in self:
            record.create_compte_in_smart()

    @api.multi
    def create_compte_in_smart(self):

        from suds.client import Client
        import os
#        _logger.info('En cours de traitement avec SmartBase...')
        print "En cours de traitement avec SmartBase..."

        partner = self.partner_id.name
        idUsager = self.partner_id.importid_SmartBambi

        folder = os.path.join(os.path.dirname(__file__), os.pardir)
        file_cfg = "file://" + os.path.abspath(folder + "/static/src/wsdl/smartIntegral.wsdl")
        c = Client(file_cfg)

        if self.school_name_id:
            monstringxmlschool = self.get_data_xml_for_school(idUsager)
            resp_school = c.service.XmlAjouterUnEvenement(Synchrone=1, donneesXml=monstringxmlschool)

        if self.half_pension:
            monstringxmlhalfpension = self.get_data_xml_for_halfpension(idUsager)
            resp_halfpension = c.service.XmlAjouterUnEvenement(Synchrone=1, donneesXml=monstringxmlhalfpension)

        if self.nursery_morning:
            monstringxmlnurserymorning = self.get_data_xml_for_nursery_morning(idUsager)
            resp_nursery_morning = c.service.XmlAjouterUnEvenement(Synchrone=1, donneesXml=monstringxmlnurserymorning)

        if self.nursery_evening:
            monstringxmlnurseryevening = self.get_data_xml_for_nursery_evening(idUsager)
            resp_nursery_evening = c.service.XmlAjouterUnEvenement(Synchrone=1, donneesXml=monstringxmlnurseryevening)

        print "communication réussie pour " + partner
#        _logger.info('communication réussie pour ', partner)

# Pour Contrats scolaire - APS - Garderie mercredi après-midi
    @api.multi
    def get_data_xml_for_school(self, idUsager):
        from datetime import date, datetime, timedelta

        # Récupère le titulaire
        idTituFoyer = self.partner_id.importid_Foyer_SmartBambi
        idTitu = idTituFoyer.split()[1].strip('[]')

        # Récupère les informations pour l'inscription scolaire
        idEtablissement = self.school_name_id.id_establishment
        idClasse = self.school_level_id.id_class

        # Récupère les différentes dates
        datedeb = datetime.strftime((datetime.now()).date(), '%m/%d/%Y %H:%M:%S')
        finComptes = (datetime.now() + timedelta(days=7300)).date()
        datefinComptes = datetime.strftime(finComptes, '%m/%d/%Y %H:%M:%S')
        debInscr = datetime.strptime(self.school_registration, "%Y-%m-%d").strftime("%m/%d/%Y")
        finInscr = self.school_end_date

        # Récupère les codes pour la grappe ContratsTerminaux
        ref_service_school = self.school_name_id.ref_service
        liste_zone_code_xml = []
        for rec_school in self.school_name_id.zone_code_ids:
            zone_code_xml_old = """<CodeZone>"""+rec_school.zone_code+"""</CodeZone>"""
            liste_zone_code_xml.append(zone_code_xml_old)
        zone_code_xml = ''.join(liste_zone_code_xml)

        ref_service_APS = self.extracurricular_activity_id.ref_service
        liste_zone_code_APS = []
        for rec_extracurricular_activity in self.extracurricular_activity_id.zone_code_ids:
            zone_code_APS_old = """<CodeZone>"""+rec_extracurricular_activity.zone_code+"""</CodeZone>"""
            liste_zone_code_APS.append(zone_code_APS_old)
        zone_code_APS = ''.join(liste_zone_code_APS)

        ref_service_wednesday_afternoon_nursery = self.nursery_wednesday_afternoon_name_id.ref_service
        liste_zone_code_wednesday_afternoon_nursery = []
        for rec_nursery in self.nursery_wednesday_afternoon_name_id.zone_code_ids:
            zone_code_wednesday_afternoon_nursery_old = """<CodeZone>"""+rec_nursery.zone_code+"""</CodeZone>"""
            liste_zone_code_wednesday_afternoon_nursery.append(zone_code_wednesday_afternoon_nursery_old)
        zone_code_wednesday_afternoon_nursery = ''.join(liste_zone_code_wednesday_afternoon_nursery)

        xmlschool = """"""
        xmlaps = """"""
        xmlnurserywednesdayafternoon = """"""

        if ref_service_school:
            xmlschool = """<ContratsTerminaux>
                        <Usager>
                            <IdUsager>"""+idUsager+"""</IdUsager>
                            <CodeContrat>0</CodeContrat>
                            <ReferencePrestation>"""+ref_service_school+"""</ReferencePrestation>
                            <DateDebutValiditeContrat>"""+debInscr+"""</DateDebutValiditeContrat>
                            <DateFinValiditeContrat>"""+finInscr+"""</DateFinValiditeContrat>
                            <Type>2</Type>
                            <ZonesServices>
                                """+zone_code_xml+"""
                            </ZonesServices>
                            <Terminaux>
                                <CodeTerminal/>
                            </Terminaux>
                        </Usager>
                  </ContratsTerminaux>"""

        if ref_service_APS and self.extracurricular_activity:
            xmlaps = """<ContratsTerminaux>
                    <Usager>
                        <IdUsager>"""+idUsager+"""</IdUsager>
                        <CodeContrat>0</CodeContrat>
                        <ReferencePrestation>"""+ref_service_APS+"""</ReferencePrestation>
                        <DateDebutValiditeContrat>"""+debInscr+"""</DateDebutValiditeContrat>
                        <DateFinValiditeContrat>"""+finInscr+"""</DateFinValiditeContrat>
                        <Type>2</Type>
                        <ZonesServices>
                            """+zone_code_APS+"""
                        </ZonesServices>
                        <Terminaux>
                            <CodeTerminal/>
                        </Terminaux>
                    </Usager>
                  </ContratsTerminaux> """

        if ref_service_wednesday_afternoon_nursery and self.nursery_wednesday_evening:
            xmlnurserywednesdayafternoon = """<ContratsTerminaux>
                    <Usager>
                        <IdUsager>"""+idUsager+"""</IdUsager>
                        <CodeContrat>0</CodeContrat>
                        <ReferencePrestation>"""+ref_service_wednesday_afternoon_nursery+"""</ReferencePrestation>
                        <DateDebutValiditeContrat>"""+debInscr+"""</DateDebutValiditeContrat>
                        <DateFinValiditeContrat>"""+finInscr+"""</DateFinValiditeContrat>
                        <Type>2</Type>
                        <ZonesServices>
                            """+zone_code_wednesday_afternoon_nursery+"""
                        </ZonesServices>
                        <Terminaux>
                            <CodeTerminal/>
                        </Terminaux>
                    </Usager>
                  </ContratsTerminaux>"""

        xml = """
            <CVQImportExport xmlns="www.horanet.com">
               <Version>2</Version>
               <CodeFournisseur>9792000100</CodeFournisseur>
               <CodeApplication>1</CodeApplication>
               <CodeTeleProcedure>0</CodeTeleProcedure>
                  <Comptes>
                      <Compte>
                         <CodeCentreGestion>49782507</CodeCentreGestion>
                         <Statut>1</Statut>
                         <IdCompte></IdCompte>
                         <IdTitulaire>"""+idTitu+"""</IdTitulaire>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebutContrat>"""+datedeb+"""</DateDebutContrat>
                         <Libelle>Cpte CCPG Periscolaire</Libelle>
                         <DateFinContrat>"""+datefinComptes+"""</DateFinContrat>
                         <TypeCompte>2</TypeCompte>
                         <CodeCatalogue>104</CodeCatalogue>
                         <Tarifs>
                            <Tarif>
                               <CodeTarif/>
                               <CodePeriodeTarifaire/>
                               <CodeDevise/>
                               <CodeProduit/>
                               <MontantTarif/>
                            </Tarif>
                         </Tarifs>
                      </Compte>
                  </Comptes>
                  """+xmlschool+"""
                  """+xmlaps+"""
                  """+xmlnurserywednesdayafternoon+"""
                  <UsagersClasseEtablissementScolaire>
                    <Usager>
                       <IdUsager>"""+idUsager+"""</IdUsager>
                       <IdClasse>"""+idClasse+"""</IdClasse>
                       <IdEtablissement>"""+idEtablissement+"""</IdEtablissement>  
                    </Usager>
                  </UsagersClasseEtablissementScolaire>
            </CVQImportExport>"""
        return xml

# Pour Restauration scolaire
    def get_data_xml_for_halfpension(self, idUsager):
        from datetime import date, datetime, timedelta

        # Récupère les identifiants de l'usager et du titulaire payeur
        # Pour idTitu, conversion de importid_Foyer_SmartBambi pour récupérer la chaîne entre crochet
        idTituFoyerHalfPension = self.half_pension_responsible_partner.importid_Foyer_SmartBambi
        idTituHalfPension = idTituFoyerHalfPension.split()[1].strip('[]')

        # Récupère les différentes dates
        datedeb = datetime.strftime((datetime.now()).date(), '%m/%d/%Y %H:%M:%S')
        finComptes = (datetime.now() + timedelta(days=7300)).date()
        datefinComptes = datetime.strftime(finComptes, '%m/%d/%Y %H:%M:%S')
        debInscrRest = datetime.strptime(self.half_pension_begin_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        finInscrRest = self.half_pension_end_date

        # Récupère le statut
        statusHalfPension = self.half_pension_status

        # Récupère la valeur binaire es jours de la semaine et mise en place dans une liste - Restauration scolaire
        bin_values_halfpension = dec2bin(self.half_pension_days_value, 7)
        list_values_halfpension = []
        for lettre in bin_values_halfpension:
            list_values_halfpension.append(lettre)

        if self.half_pension_occasional:
            monday_halfpension = "1"
            tuesday_halfpension = "1"
            wednesday_halfpension = "0"
            thursday_halfpension = "1"
            friday_halfpension = "1"
            saturday_halfpension = "0"
            sunday_halfpension = "0"
        else:
            # On sépare dans des variables nos valeurs
            monday_halfpension = list_values_halfpension[6]
            tuesday_halfpension = list_values_halfpension[5]
            wednesday_halfpension = list_values_halfpension[4]
            thursday_halfpension = list_values_halfpension[3]
            friday_halfpension = list_values_halfpension[2]
            saturday_halfpension = list_values_halfpension[1]
            sunday_halfpension = list_values_halfpension[0]

        # Récupère les codes et le libellé par rapport au lieu de restauration scolaire choisi
        code_produit_half_pension = self.half_pension_id.code_Product
        code_CDG_half_pension = self.half_pension_id.code_CDG
        code_Catalog_half_pension = self.half_pension_id.code_Catalog
        libelle_half_pension = self.half_pension_id.name

        xml = """<CVQImportExport xmlns="www.horanet.com">
                   <Version>2</Version>
                   <CodeFournisseur>9792000100</CodeFournisseur>
                   <CodeApplication>1</CodeApplication>
                   <CodeTeleProcedure>0</CodeTeleProcedure>
                   <Comptes>
                      <Compte>
                         <CodeCentreGestion>"""+code_CDG_half_pension+"""</CodeCentreGestion>
                         <Statut>1</Statut>
                         <IdCompte></IdCompte>
                         <IdTitulaire>"""+idTituHalfPension+"""</IdTitulaire>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebutContrat>"""+datedeb+"""</DateDebutContrat>
                         <Libelle>Compte Loisirs """+libelle_half_pension+"""</Libelle>
                         <DateFinContrat>"""+datefinComptes+"""</DateFinContrat>
                         <TypeCompte>2</TypeCompte>
                         <CodeCatalogue>"""+code_Catalog_half_pension+"""</CodeCatalogue>
                         <Tarifs>
                            <Tarif>
                               <CodeTarif/>
                               <CodePeriodeTarifaire/>
                               <CodeDevise/>
                               <CodeProduit/>
                               <MontantTarif/>
                            </Tarif>
                         </Tarifs>
                      </Compte>
                   </Comptes>
                   <Inscriptions>
                      <Inscription>
                         <IdCVQ/>
                         <Type>0</Type>
                         <Statut>"""+statusHalfPension+"""</Statut>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebut>"""+debInscrRest+"""</DateDebut>
                         <DateFin>"""+finInscrRest+"""</DateFin>
                         <ProfilHebdo>
                            <Lundi>"""+monday_halfpension+"""</Lundi>
                            <Mardi>"""+tuesday_halfpension+"""</Mardi>
                            <Mercredi>"""+wednesday_halfpension+"""</Mercredi>
                            <Jeudi>"""+thursday_halfpension+"""</Jeudi>
                            <Vendredi>"""+friday_halfpension+"""</Vendredi>
                            <Samedi>"""+saturday_halfpension+"""</Samedi>
                            <Dimanche>"""+sunday_halfpension+"""</Dimanche>
                         </ProfilHebdo>
                         <Id>"""+idUsager+"""</Id>
                         <CodeCentreGestionProduit>"""+code_CDG_half_pension+"""</CodeCentreGestionProduit>
                         <CodeCatalogueProduit>"""+code_Catalog_half_pension+"""</CodeCatalogueProduit>
                         <ReferenceProduitCVQ>"""+code_produit_half_pension+"""</ReferenceProduitCVQ>
                         <ReferenceProduit>"""+code_produit_half_pension+"""</ReferenceProduit>
                         <NombrePassage />
                         <PrioritesPassage>
                            <Lundi>"""+monday_halfpension+"""</Lundi>
                            <Mardi>"""+tuesday_halfpension+"""</Mardi>
                            <Mercredi>"""+wednesday_halfpension+"""</Mercredi>
                            <Jeudi>"""+thursday_halfpension+"""</Jeudi>
                            <Vendredi>"""+friday_halfpension+"""</Vendredi>
                            <Samedi>"""+saturday_halfpension+"""</Samedi>
                            <Dimanche>"""+sunday_halfpension+"""</Dimanche>
                         </PrioritesPassage>
                         <NumeroCompte>0</NumeroCompte>
                         <TypeCompte>2</TypeCompte>
                         <IdTitulaire>"""+idTituHalfPension+"""</IdTitulaire>
                         <CodeTarif/>
                      </Inscription>
                   </Inscriptions>
                </CVQImportExport>"""
        return xml

    # Pour Garderie Matin
    @api.multi
    def get_data_xml_for_nursery_morning(self, idUsager):
        from datetime import date, datetime, timedelta

        idTituFoyerNursery = self.nursery_responsible_partner.importid_Foyer_SmartBambi
        idTituNursery = idTituFoyerNursery.split()[1].strip('[]')

        # Récupère les différentes dates
        datedeb = datetime.strftime((datetime.now()).date(), '%m/%d/%Y %H:%M:%S')
        finComptes = (datetime.now() + timedelta(days=7300)).date()
        datefinComptes = datetime.strftime(finComptes, '%m/%d/%Y %H:%M:%S')
        debInscrNurs = datetime.strptime(self.nursery_begin_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        finInscrNurs = self.nursery_end_date

        # Récupère le statut
        statusNurseryMorning = self.nursery_status_morning

        # Récupère la valeur binaire en jours de la semaine et mise en place dans une liste - Garderie matin
        bin_values_nursery_morning = dec2bin(self.nursery_morning_days_value, 7)
        list_values_nursery_morning = []
        for lettre in bin_values_nursery_morning:
            list_values_nursery_morning.append(lettre)

        # On sépare dans des variables nos valeurs
        monday_nursery_morning = list_values_nursery_morning[6]
        tuesday_nursery_morning = list_values_nursery_morning[5]
        wednesday_nursery_morning = list_values_nursery_morning[4]
        thursday_nursery_morning = list_values_nursery_morning[3]
        friday_nursery_morning = list_values_nursery_morning[2]
        saturday_nursery_morning = list_values_nursery_morning[1]
        sunday_nursery_morning = list_values_nursery_morning[0]

        # Récupère les codes et le libellé par rapport au lieu de garderie choisi
        code_produit_nursery_morning = self.nursery_name_id.code_Product
        code_CDG_nursery_morning = self.nursery_name_id.code_CDG
        code_Catalog_nursery_morning = self.nursery_name_id.code_Catalog
        libelle_nursery_morning = self.nursery_name_id.name

        xml = """<CVQImportExport xmlns="www.horanet.com">
                   <Version>2</Version>
                   <CodeFournisseur>9792000100</CodeFournisseur>
                   <CodeApplication>1</CodeApplication>
                   <CodeTeleProcedure>0</CodeTeleProcedure>
                   <Comptes>
                      <Compte>
                         <CodeCentreGestion>"""+code_CDG_nursery_morning+"""</CodeCentreGestion>
                         <Statut>1</Statut>
                         <IdCompte></IdCompte>
                         <IdTitulaire>"""+idTituNursery+"""</IdTitulaire>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebutContrat>"""+datedeb+"""</DateDebutContrat>
                         <Libelle>Compte Loisirs """+libelle_nursery_morning+"""</Libelle>
                         <DateFinContrat>"""+datefinComptes+"""</DateFinContrat>
                         <TypeCompte>2</TypeCompte>
                         <CodeCatalogue>"""+code_Catalog_nursery_morning+"""</CodeCatalogue>
                         <Tarifs>
                            <Tarif>
                               <CodeTarif/>
                               <CodePeriodeTarifaire/>
                               <CodeDevise/>
                               <CodeProduit/>
                               <MontantTarif/>
                            </Tarif>
                         </Tarifs>
                      </Compte>
                   </Comptes>
                   <Inscriptions>
                      <Inscription>
                         <IdCVQ/>
                         <Type>0</Type>
                         <Statut>"""+statusNurseryMorning+"""</Statut>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebut>"""+debInscrNurs+"""</DateDebut>
                         <DateFin>"""+finInscrNurs+"""</DateFin>
                         <ProfilHebdo>
                            <Lundi>"""+monday_nursery_morning+"""</Lundi>
                            <Mardi>"""+tuesday_nursery_morning+"""</Mardi>
                            <Mercredi>"""+wednesday_nursery_morning+"""</Mercredi>
                            <Jeudi>"""+thursday_nursery_morning+"""</Jeudi>
                            <Vendredi>"""+friday_nursery_morning+"""</Vendredi>
                            <Samedi>"""+saturday_nursery_morning+"""</Samedi>
                            <Dimanche>"""+sunday_nursery_morning+"""</Dimanche>
                         </ProfilHebdo>
                         <Id>"""+idUsager+"""</Id>
                         <CodeCentreGestionProduit>"""+code_CDG_nursery_morning+"""</CodeCentreGestionProduit>
                         <CodeCatalogueProduit>"""+code_Catalog_nursery_morning+"""</CodeCatalogueProduit>
                         <ReferenceProduitCVQ>"""+code_produit_nursery_morning+"""</ReferenceProduitCVQ>
                         <ReferenceProduit>"""+code_produit_nursery_morning+"""</ReferenceProduit>
                         <NombrePassage />
                         <PrioritesPassage>
                            <Lundi>"""+monday_nursery_morning+"""</Lundi>
                            <Mardi>"""+tuesday_nursery_morning+"""</Mardi>
                            <Mercredi>"""+wednesday_nursery_morning+"""</Mercredi>
                            <Jeudi>"""+thursday_nursery_morning+"""</Jeudi>
                            <Vendredi>"""+friday_nursery_morning+"""</Vendredi>
                            <Samedi>"""+saturday_nursery_morning+"""</Samedi>
                            <Dimanche>"""+sunday_nursery_morning+"""</Dimanche>
                         </PrioritesPassage>
                         <NumeroCompte>0</NumeroCompte>
                         <TypeCompte>2</TypeCompte>
                         <IdTitulaire>"""+idTituNursery+"""</IdTitulaire>
                         <CodeTarif/>
                      </Inscription>
                   </Inscriptions>
                </CVQImportExport>"""
        return xml

    # Pour Garderie soir
    @api.multi
    def get_data_xml_for_nursery_evening(self, idUsager):
        from datetime import date, datetime, timedelta

        idTituFoyerNursery = self.nursery_responsible_partner.importid_Foyer_SmartBambi
        idTituNursery = idTituFoyerNursery.split()[1].strip('[]')

        # Récupère les différentes dates
        datedeb = datetime.strftime((datetime.now()).date(), '%m/%d/%Y %H:%M:%S')
        finComptes = (datetime.now() + timedelta(days=7300)).date()
        datefinComptes = datetime.strftime(finComptes, '%m/%d/%Y %H:%M:%S')
        debInscrNurs = datetime.strptime(self.nursery_begin_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        finInscrNurs = self.nursery_end_date

        # Récupère le statut
        statusNurseryevening = self.nursery_status_evening

        # Récupère la valeur binaire en jours de la semaine et mise en place dans une liste - Garderie soir
        bin_values_nursery_evening = dec2bin(self.nursery_evening_days_value, 7)
        list_values_nursery_evening = []
        for lettre in bin_values_nursery_evening:
            list_values_nursery_evening.append(lettre)

        # On sépare dans des variables nos valeurs
        monday_nursery_evening = list_values_nursery_evening[6]
        tuesday_nursery_evening = list_values_nursery_evening[5]
        wednesday_nursery_evening = list_values_nursery_evening[4]
        thursday_nursery_evening = list_values_nursery_evening[3]
        friday_nursery_evening = list_values_nursery_evening[2]
        saturday_nursery_evening = list_values_nursery_evening[1]
        sunday_nursery_evening = list_values_nursery_evening[0]

        # Récupère les codes et le libellé par rapport au lieu de garderie choisi
        code_produit_nursery_evening = self.nursery_two_name_id.code_Product
        code_CDG_nursery_evening = self.nursery_two_name_id.code_CDG
        code_Catalog_nursery_evening = self.nursery_two_name_id.code_Catalog
        libelle_nursery_evening = self.nursery_two_name_id.name

        xml = """<CVQImportExport xmlns="www.horanet.com">
                   <Version>2</Version>
                   <CodeFournisseur>9792000100</CodeFournisseur>
                   <CodeApplication>1</CodeApplication>
                   <CodeTeleProcedure>0</CodeTeleProcedure>
                   <Comptes>
                      <Compte>
                         <CodeCentreGestion>"""+code_CDG_nursery_evening+"""</CodeCentreGestion>
                         <Statut>1</Statut>
                         <IdCompte></IdCompte>
                         <IdTitulaire>"""+idTituNursery+"""</IdTitulaire>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebutContrat>"""+datedeb+"""</DateDebutContrat>
                         <Libelle>Compte Loisirs """+libelle_nursery_evening+"""</Libelle>
                         <DateFinContrat>"""+datefinComptes+"""</DateFinContrat>
                         <TypeCompte>2</TypeCompte>
                         <CodeCatalogue>"""+code_Catalog_nursery_evening+"""</CodeCatalogue>
                         <Tarifs>
                            <Tarif>
                               <CodeTarif/>
                               <CodePeriodeTarifaire/>
                               <CodeDevise/>
                               <CodeProduit/>
                               <MontantTarif/>
                            </Tarif>
                         </Tarifs>
                      </Compte>
                   </Comptes>
                   <Inscriptions>
                      <Inscription>
                         <IdCVQ/>
                         <Type>0</Type>
                         <Statut>"""+statusNurseryevening+"""</Statut>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebut>"""+debInscrNurs+"""</DateDebut>
                         <DateFin>"""+finInscrNurs+"""</DateFin>
                         <ProfilHebdo>
                            <Lundi>"""+monday_nursery_evening+"""</Lundi>
                            <Mardi>"""+tuesday_nursery_evening+"""</Mardi>
                            <Mercredi>"""+wednesday_nursery_evening+"""</Mercredi>
                            <Jeudi>"""+thursday_nursery_evening+"""</Jeudi>
                            <Vendredi>"""+friday_nursery_evening+"""</Vendredi>
                            <Samedi>"""+saturday_nursery_evening+"""</Samedi>
                            <Dimanche>"""+sunday_nursery_evening+"""</Dimanche>
                         </ProfilHebdo>
                         <Id>"""+idUsager+"""</Id>
                         <CodeCentreGestionProduit>"""+code_CDG_nursery_evening+"""</CodeCentreGestionProduit>
                         <CodeCatalogueProduit>"""+code_Catalog_nursery_evening+"""</CodeCatalogueProduit>
                         <ReferenceProduitCVQ>"""+code_produit_nursery_evening+"""</ReferenceProduitCVQ>
                         <ReferenceProduit>"""+code_produit_nursery_evening+"""</ReferenceProduit>
                         <NombrePassage />
                         <PrioritesPassage>
                            <Lundi>"""+monday_nursery_evening+"""</Lundi>
                            <Mardi>"""+tuesday_nursery_evening+"""</Mardi>
                            <Mercredi>"""+wednesday_nursery_evening+"""</Mercredi>
                            <Jeudi>"""+thursday_nursery_evening+"""</Jeudi>
                            <Vendredi>"""+friday_nursery_evening+"""</Vendredi>
                            <Samedi>"""+saturday_nursery_evening+"""</Samedi>
                            <Dimanche>"""+sunday_nursery_evening+"""</Dimanche>
                         </PrioritesPassage>
                         <NumeroCompte>0</NumeroCompte>
                         <TypeCompte>2</TypeCompte>
                         <IdTitulaire>"""+idTituNursery+"""</IdTitulaire>
                         <CodeTarif/>
                      </Inscription>
                   </Inscriptions>
                </CVQImportExport>"""
        return xml

# Appel cette méthode quand on créé un nouvel enregistrement
    @api.model
    def create(self, vals):
        record = super(ResPartnerSchool, self).create(vals)
        record.no_duplicate_school_dates()
        # Permet de ne pas appelé cette fonction si c'est une importation de données
        if not self.env.context.get('tracking_disable'):
            record.smart_synchronization()
        return record

# Appel cette méthode quand on modifie un enregistrement
    @api.multi
    def write(self, vals):
        result = super(ResPartnerSchool, self).write(vals)
        self.no_duplicate_school_dates()
        if not self.env.context.get('tracking_disable'):
            self.smart_synchronization()
        return result
