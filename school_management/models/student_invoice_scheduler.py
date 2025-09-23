from datetime import date
from odoo import models, api

class StudentInvoiceScheduler(models.Model):
    _inherit = 'school.student'

    @api.model
    def cron_generate_monthly_invoices(self):
        """
        Scheduler untuk membuat tagihan bulanan otomatis untuk semua siswa aktif.
        - Berjalan tiap awal bulan.
        - Cek apakah siswa sudah punya invoice untuk bulan berjalan.
        - Jika belum, buat invoice baru.
        """
        today = date.today()
        billing_period = today.strftime('%Y-%m')  # contoh: 2025-10

        # ambil product type : servie , "Biaya Sekolah Bulanan"
        product = self.env['product.product'].search([('name', '=', 'Biaya Sekolah Bulanan')], limit=1)
        if not product:
            raise ValueError("Product 'Biaya Sekolah Bulanan' tidak ditemukan. Harap buat dulu di Odoo.")

        students = self.search([('active', '=', True)])
        AccountMove = self.env['account.move']

        for student in students:
            # Cek apakah sudah ada invoice untuk periode ini
            existing_invoice = AccountMove.search([
                ('student_id', '=', student.id),
                ('billing_period', '=', billing_period),
                ('is_tuition_invoice', '=', True),
            ], limit=1)

            if existing_invoice:
                continue  # Skip jika sudah ada invoice bulan ini

            # Buat invoice baru
            AccountMove.create({
                'move_type': 'out_invoice',
                'partner_id': student.partner_id.id,
                'student_id': student.id,
                'billing_period': billing_period,
                'is_tuition_invoice': True,
                'invoice_line_ids': [(0, 0, {
                    'product_id': product.id,
                    'quantity': 1,
                    'price_unit': product.list_price,
                })],
            })
