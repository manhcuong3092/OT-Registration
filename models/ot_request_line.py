import datetime

from odoo import models, fields, api, _


class OTRequestLine(models.Model):
    _name = "ot.request.line"
    _description = "OT Request Line"

    name = fields.Char('Request line order', require=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    ot_from = fields.Datetime('From')
    ot_to = fields.Datetime('To')
    wfh = fields.Boolean('WFH')
    ot_hours = fields.Float('OT Hours', compute='_compute_ot_hours', digits=(12,1), readonly=True, store=True)
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
    employee_id_related = fields.Many2one('hr.employee', string='Employee', related='ot_registration_id.employee_id')
    project_id_related = fields.Many2one('project.project', string='Project', related='ot_registration_id.project_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ot.request.line') or _('New')
        res = super(OTRequestLine, self).create(vals)
        return res

    @api.depends('ot_from', 'ot_to')
    def _compute_ot_hours(self):
        sec_per_hour = 3600
        for rec in self:
            if rec.ot_to and rec.ot_from:
                delta = rec.ot_to - rec.ot_from
                rec.ot_hours = round(delta.total_seconds() / sec_per_hour, 1)

    def action_submit(self):
        self.state = 'to_approve'

    def action_pm_approve(self):
        self.state = 'pm_approved'

    def action_dl_approve(self):
        self.state = 'dl_approved'

    def action_refuse(self):
        self.state = 'refused'

    def action_draft(self):
        self.state = 'draft'
