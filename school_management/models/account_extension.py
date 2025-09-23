# -*- coding: utf-8 -*-
"""
Extend model Account Move (Invoice) untuk menambahkan relasi ke Student.

Fungsi:
--------
1. Menghubungkan invoice dengan student (`school.student`).
2. Menambahkan field `billing_period` untuk identifikasi periode tagihan.
"""

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one(
        comodel_name='school.student',
        string='Student',
        ondelete='set null',
        help="Siswa yang terkait dengan invoice ini."
    )

    billing_period = fields.Char(
        string='Billing Period',
        help="Periode penagihan dalam format YYYY-MM, contoh: 2025-09."
    )

    is_tuition_invoice = fields.Boolean(string="Tuition Invoice", default=False)