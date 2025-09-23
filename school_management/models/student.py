# -*- coding: utf-8 -*-
"""
Model Student untuk modul School Management.

Fungsi:
--------
1. Menyimpan informasi siswa seperti nama, tanggal lahir, status aktif, dan catatan.
2. Relasi ke Kelas (school.class) untuk menentukan siswa berada di kelas mana.
3. Relasi ke Partner (res.partner) agar bisa dibuatkan invoice.
4. Menyimpan daftar invoice yang terkait siswa ini.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    """
    Model untuk menyimpan data siswa.

    Tabel yang dihasilkan di database: `school_student`
    """
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'name'
    _order = 'name ASC'

    # ==============================
    # FIELD DEFINITIONS
    # ==============================

    name = fields.Char(
        string='Nama Siswa',
        required=True,
        help="Nama lengkap siswa. Field ini wajib diisi."
    )

    dob = fields.Date(
        string='Tanggal Lahir',
        help="Tanggal lahir siswa."
    )

    # Relasi ke partner untuk invoicing
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Orang Tua/Wali',
        help="Partner yang bertanggung jawab atas pembayaran siswa."
    )

    # Relasi ke kelas
    class_id = fields.Many2one(
        comodel_name='school.class',
        string='Kelas',
        ondelete='set null',
        help="Kelas tempat siswa ini terdaftar."
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help="Status aktif siswa ini. Jika non-aktif, siswa tidak akan ditagih."
    )

    note = fields.Text(
        string='Catatan',
        help="Catatan tambahan mengenai siswa ini."
    )

    # Relasi ke invoice (account.move) → di-extend
    invoice_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='student_id',
        string='Daftar Invoice',
        help="Daftar invoice yang terkait dengan siswa ini."
    )

    # CONSTRAINTS
    @api.constrains('dob')
    def _check_dob(self):
        """
        Validasi opsional:
        - Pastikan tanggal lahir tidak di masa depan.
        """
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError("Tanggal lahir tidak boleh di masa depan.")

    # HELPER METHODS
    def name_get(self):
        """
        Custom display name untuk siswa.
        Format: 'Nama Siswa (Kelas)'
        """
        result = []
        for rec in self:
            display = rec.name
            if rec.class_id:
                display = f"{rec.name} ({rec.class_id.name})"
            result.append((rec.id, display))
        return result
