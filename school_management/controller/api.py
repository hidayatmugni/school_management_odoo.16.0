# -*- coding: utf-8 -*-
"""
REST API Controller untuk modul School Management.
Endpoint ini digunakan untuk mendapatkan daftar guru.

Method: GET
URL: /api/teachers

Method: POST
URL: /api/Students
"""

from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)


class SchoolAPIController(http.Controller):

    @http.route('/api/teachers', type='http', auth='public', methods=['GET'], csrf=False)
    def get_teachers(self):
        """
        Endpoint untuk mengambil daftar guru dalam format JSON.
        Bisa diuji lewat Postman: GET http://localhost:8069/api/teachers
        """
        try:
            # Ambil semua data guru yang masih aktif
            teachers = request.env['school.teacher'].sudo().search([])

            # Format response
            data = []
            for teacher in teachers:
                data.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "phone": teacher.phone or "",
                    "email": teacher.email or "",
                    "student_count": teacher.student_count,  # dihitung otomatis
                })

            # Return JSON response
            response_body = json.dumps({
                "status": "success",
                "count": len(data),
                "data": data
            }, indent=4)

            return Response(
                response=response_body,
                status=200,
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            # Jika ada error, return error response
            error_body = json.dumps({
                "status": "error",
                "message": str(e)
            }, indent=4)

            return Response(
                response=error_body,
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    # POST TAMBAH SISWA BARU
    @http.route('/api/students', type='http', auth='public', methods=['POST'], csrf=False)
    def create_student_http(self):
        try:
            # Ambil raw data dari body
            raw_data = request.httprequest.data.decode('utf-8')
            payload = json.loads(raw_data) if raw_data else {}

            # Validasi field yang wajib diisi
            required_fields = ['name', 'dob', 'class_id', 'partner_id']
            for field in required_fields:
                if field not in payload:
                    return Response(
                        json.dumps({"status": "error", "message": f"Field '{field}' wajib diisi!"}),
                        content_type='application/json',
                        status=400
                    )

            # Validasi class_id & partner_id
            kelas = request.env['school.class'].sudo().browse(payload['class_id'])
            partner = request.env['res.partner'].sudo().browse(payload['partner_id'])
            if not kelas.exists():
                return Response(json.dumps({"status": "error", "message": "Class ID tidak ditemukan"}),
                                content_type='application/json', status=404)
            if not partner.exists():
                return Response(json.dumps({"status": "error", "message": "Partner ID tidak ditemukan"}),
                                content_type='application/json', status=404)

            # Buat siswa
            student = request.env['school.student'].sudo().create({
                'name': payload['name'],
                'dob': payload['dob'],
                'class_id': payload['class_id'],
                'partner_id': payload['partner_id'],
                'active': True
            })

            return Response(
                json.dumps({
                    "status": "success",
                    "message": "Siswa berhasil ditambahkan",
                    "data": {
                        "id": student.id,
                        "name": student.name,
                        "dob": str(student.dob),
                        "class_name": student.class_id.name,
                        "partner_name": student.partner_id.name
                    }
                }),
                content_type='application/json',
                status=200
            )
        
        except Exception as e:
            return Response(
                json.dumps({"status": "error", "message": str(e)}),
                content_type='application/json',
                status=500
            )
