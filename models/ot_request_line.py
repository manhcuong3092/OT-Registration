import datetime

from odoo import models, fields, api


class OTRequestLine(models.Model):
    _name = "ot.request.line"
    _description = "OT Request Line"

    ot_from = fields.Datetime('From')
    ot_to = fields.Datetime('To')
    wfh = fields.Boolean('WFH')
    ot_hours = fields.Integer('OT Hours', compute='_compute_ot_hours', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved'),
                              ('refused', 'Refused')],
                             default='draft', string='State', tracking=True)
    late_approved = fields.Boolean('Late Approved')
    job_taken = fields.Char('Job Taken')
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

    @api.onchange('ot_from', 'ot_to')
    def _compute_ot_hours(self):
        for rec in self:
            if rec.ot_to and rec.ot_from:
                delta = rec.ot_to - rec.ot_from
                rec.ot_hours = round((delta/datetime.timedelta(hours=1)), 1)
