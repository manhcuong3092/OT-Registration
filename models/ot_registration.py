from odoo import models, fields


class OTRegistration(models.Model):
    _name = 'ot.registration'
    _description = 'OT Registration'

    employee_id = fields.Many2one('res.users', 'Employee', default=lambda self: self.env.user, readonly=True)
    project_id = fields.Many2one('project.project', string='Project')
    approver_id = fields.Many2one('hr.employee', string="Approver")
    department_lead_id = fields.Many2one('hr.employee', string='Department Lead',
                                         related='employee_id.department_id.manager_id',
                                         readonly=True)
    created_date = fields.Datetime('Created date', readonly=True, default=lambda self: fields.datetime.now())
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved')],
                             default='draft', string='Status', tracking=True)


class OTRequestLine(models.Model):
    _name = "ot.request.line"
    _description = "OT Request Line"

    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved')],
                             default='draft', string='Status', tracking=True)

    ot_from = fields.Datetime('From')
    ot_to = fields.Datetime('To')
    wfh = fields.Boolean('WFH')
    ot_hours = fields.Integer('OT Hours')
    state = fields.Char('State')
    late_approved = fields.Boolean('Late Approved')
    hr_note = fields.Char('Hr notes')
    attendance_note = fields.Char('Attendance notes')
    warning = fields.Char('Warning')
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
    ot_registration_id = fields.Many2one('ot.registration', string='OT Registration')
