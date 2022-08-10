import datetime

from odoo import models, fields, api, _


class OTRegistration(models.Model):
    _name = 'ot.registration'
    _description = 'OT Registration'
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char('Request line order', require=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    employee_id = fields.Many2one('hr.employee', 'Employee', default=_get_employee_id, readonly=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    project_manager_id = fields.Many2one('hr.employee', string='Project Manager')
    approver_id = fields.Many2one('hr.employee', string="Approver", store='True')
    department_lead_id = fields.Many2one('hr.employee', string='Department Lead',
                                         related='employee_id.department_id.manager_id',
                                         readonly=True)
    created_date = fields.Datetime('Created date', readonly=True, default=lambda self: fields.datetime.now())
    total_ot = fields.Integer('OT Hours', compute='_compute_total_ot', readonly=True, store=True)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved'),
                              ('refused', 'Refused')],
                             default='draft', string='Status', tracking=True)
    ot_request_line_ids = fields.One2many('ot.request.line', 'ot_registration_id',
                                          string='OT Request Line')
    ot_month = fields.Char('OT Month', compute='_compute_ot_months', readonly=True, store=True)

    @api.depends('ot_request_line_ids')
    def _compute_total_ot(self):
        total_ot = 0
        sec_per_hour = 3600
        for rec in self.ot_request_line_ids:
            if rec.ot_to and rec.ot_from:
                delta = rec.ot_to - rec.ot_from
                total_ot += round(delta.total_seconds() / sec_per_hour, 1)
        self.total_ot = total_ot

    @api.depends('ot_request_line_ids')
    def _compute_ot_months(self):
        for rec in self.ot_request_line_ids:
            if rec.ot_to and rec.ot_from:
                self.ot_month = str(rec.ot_from.month) + '/' + str(rec.ot_to.year)
                break

    def check_valid_ot(self):
        for rec in self.ot_request_line_ids:
            if rec.ot_to and rec.ot_from:
                delta = rec.ot_from - datetime.datetime.now()
                if delta.days < 2:
                    return {'valid': False, 'message': 'Datetime OT from must be before 2 days from now',
                            'type': 'danger'}
                delta = rec.ot_to - rec.ot_from
                ot_hours = round((delta / datetime.timedelta(hours=1)), 1)
                if ot_hours <= 0:
                    return {'valid': False, 'message': 'OT Hours must be greater than 0', 'type': 'danger'}
            else:
                return {'valid': False, 'message': 'Empty field ot_from or ot_to', 'type': 'danger'}
        return {'valid': True, 'message': 'Submit successfully!', 'type': 'success'}

    def action_submit(self):
        if self.ot_request_line_ids:
            check = self.check_valid_ot()
            if check['valid']:
                self.state = 'to_approve'
                template = self.env.ref('ot_registration.ot_registration_email_request_pm_template')
                template.send_mail(self.id, force_send=True)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': check['message'],
                    'type': check['type'],
                    'sticky': False
                }
            }
        else:
            message = 'OT registration must have 1 request line'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message,
                    'type': 'danger',
                    'sticky': True
                }
            }

    def action_pm_approve(self):
        self.state = 'pm_approved'
        template = self.env.ref('ot_registration.ot_registration_email_request_dl_template')
        template.send_mail(self.id, force_send=True)

    def action_dl_approve(self):
        self.state = 'dl_approved'
        template = self.env.ref('ot_registration.ot_registration_email_dl_approved_template')
        template.send_mail(self.id, force_send=True)

    def action_pm_refuse(self):
        self.state = 'refused'
        template = self.env.ref('ot_registration.ot_registration_email_pm_refused_template')
        template.send_mail(self.id, force_send=True)

    def action_dl_refuse(self):
        self.state = 'refused'
        template = self.env.ref('ot_registration.ot_registration_email_dl_refused_template')
        template.send_mail(self.id, force_send=True)

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ot.registration') or _('New')
        res = super(OTRegistration, self).create(vals)
        return res

    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.project_id and self.project_id.user_id and self.project_id.user_id.employee_id:
            self.project_manager_id = self.project_id.user_id.employee_id.id
