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
    total_ot = fields.Integer('OT Hours')
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved'),
                              ('refused', 'Refused')],
                             default='draft', string='Status', tracking=True)
    ot_request_line_ids = fields.One2many('ot.request.line', 'ot_registration_id',
                                          string='OT Request Line')

    def action_submit(self):
        self.state = 'to_approve'
        template = self.env.ref('ot_registration.ot_registration_email_request_pm_template')
        template.send_mail(self.id, force_send=True)

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
