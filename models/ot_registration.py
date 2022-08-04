from odoo import models, fields


class RegisterOT(models.Model):
    _name = 'ot.registration'
    _description = 'OT Registration'

    def _get_default_dl(self):
        return self.env['hr.employee'].search([('??', '=', '??')], limit=1).id

    employee_id = fields.Many2one('res.users', 'Employee', default=lambda self: self.env.user, readonly=True)
    project_id = fields.Many2one('project.project', string='Project')
    # department_id = fields.Many2one('hr.department', string='Department',
    #                                 default=lambda self: self.env.user.department_id,
    #                                 readonly=True)
    approver_id = fields.Many2one('hr.employee', string="Approver", related='employee_id.department_id.manager_id.')
    department_lead_id = fields.Many2one('hr.employee', string='Department Lead', related='department_id.manager_id',
                                         readonly=True, tracking=True)
    created_date = fields.Datetime('Created date', readonly=True, default=lambda self: fields.datetime.now())

    ot_from = fields.Datetime('From')
    ot_to = fields.Datetime('To')
    category = fields.Selection(selection=[('normal_day', 'Ngày bình thường'),
                                           ('normal_day_morning', 'OT ban ngày (6h - 8h30)'),
                                           ('normal_day_night', 'Ngày bình thường - Ban đêm'),
                                           ('saturday', 'Thứ 7'),
                                           ('sunday', 'Chủ nhật'),
                                           ('weekend_day_night', 'Ngày cuối tuần - Ban đêm'),
                                           ('holiday', 'Ngày lễ'),
                                           ('holiday_day_night', 'Ngày lễ - Ban đêm'),
                                           ('compensatory_normal', 'Bù ngày lễ vào ngày thường'),
                                           ('compensatory_night', 'Bù ngày lễ vào ban đêm')], default='normal_day',
                                required=True,
                                track_visibility='onchange', string='OT Category')
    # wfh = fields.Boolean('WFH')
    # ot_hours = fields.Integer('OT hours')
    # state = fields.Char('State')
    # late_approved = fields.Boolean('Late Approved')
    # hr_note = fields.Char('Hr notes')
    # attendance_note = fields.Char('Attendance notes')
    # warning = fields.Char('Warning')
