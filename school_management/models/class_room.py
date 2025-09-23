# -*- coding: utf-8 -*-
"""
Model Class untuk modul School Management.

Fungsi:
--------
1. Menyimpan informasi kelas, seperti nama kelas, kapasitas, dan jadwal.
2. Relasi dengan Guru (school.teacher) untuk mengetahui siapa yang mengajar kelas ini.
3. Relasi dengan Siswa (school.student) untuk mengetahui daftar siswa dalam kelas.
"""

from odoo import models, fields


class SchoolClass(models.Model):
    """
    Model untuk menyimpan data kelas.
    
    Tabel yang dihasilkan di database: `school_class`
    """
    _name = 'school.class'
    _description = 'Class'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Nama Kelas',
        required=True,
        help="Nama kelas, contoh: Kelas 1A, 2B, dsb."
    )

    code = fields.Char(
        string='Kode Kelas',
        help="Kode unik untuk kelas, contoh: 1A-2025."
    )

    # Relasi ke Guru
    teacher_id = fields.Many2one(
        comodel_name='school.teacher',
        string='Guru Pengajar',
        ondelete='set null',
        help="Guru yang mengajar kelas ini."
    )

    # Relasi ke Siswa
    student_ids = fields.One2many(
        comodel_name='school.student',
        inverse_name='class_id',
        string='Daftar Siswa',
        help="Daftar siswa yang terdaftar dalam kelas ini."
    )

    capacity = fields.Integer(
        string='Kapasitas',
        help="Jumlah maksimal siswa yang dapat diterima dalam kelas ini."
    )

    schedule = fields.Text(
        string='Jadwal',
        help="Informasi jadwal pelajaran untuk kelas ini."
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help="Status aktif kelas ini."
    )

    note = fields.Text(
        string='Catatan',
        help="Catatan tambahan terkait kelas ini."
    )

    # HELPER METHODS
    def name_get(self):
        """
        Custom display name untuk kelas.
        Format: 'Nama Kelas (Guru)'
        """
        result = []
        for rec in self:
            display = rec.name
            if rec.teacher_id:
                display = f"{rec.name} ({rec.teacher_id.name})"
            result.append((rec.id, display))
        return result
