# -*- coding: utf-8 -*-
"""
Model Teacher untuk modul School Management.

Fungsi:
--------
1. Menyimpan data guru seperti nama, alamat, nomor telepon, dan status aktif.
2. Menyimpan relasi dengan model Class (`school.class`) untuk mengetahui
   kelas yang diajar guru tersebut.
3. Menyediakan field `student_count` yang otomatis menghitung total siswa
   yang diajar oleh guru melalui relasi kelas.
4. Menyediakan validasi unik untuk nomor telepon agar tidak ada duplikasi.
5. Menyediakan tombol aksi (object button) untuk mengaktifkan/nonaktifkan
   semua siswa yang terkait guru ini.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class SchoolTeacher(models.Model):
    """
    Model utama untuk menyimpan data guru (Teacher).
    
    Tabel yang dihasilkan di database: `school_teacher`
    """
    _name = 'school.teacher'
    _description = 'Teacher'
    _rec_name = 'name'
    _order = 'name ASC'

    # ==============================
    # FIELD DEFINITIONS
    # ==============================

    name = fields.Char(
        string='Nama Guru',
        required=True,
        help="Nama lengkap guru. Field ini wajib diisi."
    )

    address = fields.Text(
        string='Alamat',
        help="Alamat lengkap guru untuk kebutuhan administrasi."
    )

    phone = fields.Char(
        string='Nomor Telepon',
        required=True,
        help="Nomor telepon guru. Harus unik dan tidak boleh duplikat."
    )

    email = fields.Char(
        string='Email',
        help="Alamat email guru untuk komunikasi."
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help="Status aktif guru. Jika tidak aktif, guru ini dianggap non-aktif."
    )

    # Relasi ke model Class (school.class)
    class_ids = fields.One2many(
        comodel_name='school.class',
        inverse_name='teacher_id',
        string='Daftar Kelas',
        help="Daftar kelas yang diajar oleh guru ini."
    )

    # Field untuk menyimpan total siswa yang diajar guru
    student_count = fields.Integer(
        string='Jumlah Siswa',
        compute='_compute_student_count',
        store=True,
        help="Total siswa yang diajar oleh guru ini, dihitung otomatis."
    )

    note = fields.Text(
        string='Catatan',
        help="Catatan tambahan terkait guru."
    )

    # SQL CONSTRAINTS pada database
    _sql_constraints = [
        (
            'phone_unique',
            'unique(phone)',     
            'Nomor telepon sudah digunakan oleh guru lain.' 
        ),
    ]

    # COMPUTE METHODS
    @api.depends('class_ids.student_ids')
    def _compute_student_count(self):
        """
        Menghitung jumlah siswa yang diajar oleh guru ini.

        Logic:
        - Ambil semua kelas yang terkait guru.
        - Hitung jumlah total siswa (student_ids) dalam semua kelas tersebut.
        """
        for teacher in self:
            total_students = 0
            for school_class in teacher.class_ids:
                total_students += len(school_class.student_ids)
            teacher.student_count = total_students

    # CONSTRAINS di ui
    @api.constrains('phone')
    def _check_unique_phone(self):
        """
        Validasi tambahan untuk memastikan nomor telepon guru unik.
        - Akan melempar ValidationError jika ditemukan duplikasi.
        """
        for record in self:
            # Cari record lain dengan phone yang sama, selain current record
            duplicate = self.search([
                ('phone', '=', record.phone),
                ('id', '!=', record.id)
            ])
            if duplicate:
                raise ValidationError(
                    "Nomor telepon '%s' sudah digunakan oleh guru lain." % record.phone
                )

    # BUTTON / ACTION METHODS
    def action_toggle_students_active(self):
        """
        Tombol aksi untuk toggle semua siswa yang diajar guru ini.
        - Jika semua siswa aktif → set menjadi nonaktif (archive).
        - Jika ada yang nonaktif → set semuanya aktif (unarchive).
        """
        Student = self.env['school.student'].with_context(active_test=False)  # agar bisa melihat siswa yang inactive juga

        for teacher in self:
            # Cari semua siswa dari kelas yang diajar guru yang sesuai
            students = Student.search([('class_id.teacher_id', '=', teacher.id)])

            if not students:
                # Jika guru ini belum punya siswa, raise UserError sebagai peringatan
                raise UserError(f"Tidak ada siswa yang terdaftar di kelas {teacher.name}.")

            # Cek apakah semua siswa aktif
            all_active = all(students.mapped('active'))

            # Toggle status
            students.write({'active': not all_active})

            # RETURN NOTIFICATION KE UI
            if all_active:
                # Semua siswa tadinya aktif → sekarang dinonaktifkan
                message = f"Semua siswa yang diajar oleh {teacher.name} berhasil di-nonaktifkan."
                title = "Siswa Dinonaktifkan"
            else:
                # Ada siswa yang tadinya nonaktif → sekarang diaktifkan
                message = f"Semua siswa yang diajar oleh {teacher.name} berhasil diaktifkan kembali."
                title = "Siswa Diaktifkan"

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'sticky': False, 
                    'type': 'success' if not all_active else 'warning'
                }
            }

    # NAME GET 
    def name_get(self):
        """
        Custom display name untuk guru.
        Contoh output: "Budi - 08123456789"
        """
        result = []
        for rec in self:
            display = f"{rec.name} - {rec.phone}" if rec.phone else rec.name
            result.append((rec.id, display))
        return result
