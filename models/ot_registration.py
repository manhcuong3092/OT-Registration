from odoo import models, fields


class OTRegistration(models.Model):
    _name = 'ot.registration'
    _description = 'OT Registration'
    _inherit = ["mail.thread", 'mail.activity.mixin']

    employee_id = fields.Many2one('res.users', 'Employee', default=lambda self: self.env.user, readonly=True)
    project_id = fields.Many2one('project.project', string='Project')
    approver_id = fields.Many2one('hr.employee', string="Approver")
    department_lead_id = fields.Many2one('hr.employee', string='Department Lead',
                                         related='employee_id.department_id.manager_id',
                                         readonly=True)
    created_date = fields.Datetime('Created date', readonly=True, default=lambda self: fields.datetime.now())
    total_ot = fields.Integer('OT Hours')
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved')],
                             default='draft', string='Status', tracking=True)
    ot_request_line_ids = fields.One2many('ot.request.line', 'ot_registration_id',
                                            string='OT Request Line')

    def action_submit(self):
        self.state = 'to_approve'
