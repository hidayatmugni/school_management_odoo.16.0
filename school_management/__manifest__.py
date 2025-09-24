# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'version': '16.0.1.0.0',
    'category': 'Education',
    'summary': 'Manage teachers, classes, and students with invoicing',
    'description': """
        School Management
        =================
        - Manage teachers, classes, and students
        - Auto-generate monthly invoices
        - API integration for external systems
    """,
    'author': 'Mugni Hidayat',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'contacts', 'mail', 'product'],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Reports
        'reports/teacher_report.xml',
        'reports/receipt_report.xml',
        # views
        'views/teacher_views.xml',
        'views/class_views.xml',
        'views/student_views.xml',
        'views/account_move_views.xml',
        'views/menu_actions.xml',
        # data
        'data/ir_cron.xml',
    ],
    'demo': [
        # 'data/demo_data.xml',
        # data demo saya belum berhasil pak, ga sempat diperbaiki dikarenakan masalah waktu
        # Terima kasih pak atas kesempatan nya ...
    ],
    'installable': True,
    'application': True,
}
