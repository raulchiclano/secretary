# -*- coding: utf-8 -*-

import string
from odoo import models, fields, api
from datetime import date


def get_years(): 
    year_list = [] 
    for i in range(2022, 2050): 
        year_list.append((str(i), str(i))) 
    return year_list

class publicadores(models.Model):
     _name = 'secretary.publicadores'
     _description = 'Publicadores'

     name = fields.Char(string='Nombre completo', default="apellidos, nombre", required=True)
     fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
     fecha_bautismo = fields.Date(string='Fecha de bautismo')
     telefono = fields.Integer(string='Teléfono')
     genero = fields.Selection([('H','Hombre'), ('M','Mujer')], string='Género')
     direccion = fields.Char(string='Dirección')
     tipo = fields.Selection([('P','Publicador'), ('A', 'Auxiliar'), ('R','Regular')], string='Tipo', required=True)
     grupo = fields.Many2one(string='Grupo de Servicio', comodel_name="secretary.grupos")
     email = fields.Char(string='Email')
     image = fields.Binary(string='Imagen')


class grupos(models.Model):
    _name = 'secretary.grupos'
    _description = 'Grupos de Servicio'

    name = fields.Char(string='Nombre')

    def f_create(self):
        grupo = {
            'name': 'Test',
        }

        self.env['secretary.grupos'].create(grupo)

class informes(models.Model):
     _name = 'secretary.informes'
     _description = 'Informe de predicación'
     
     nombre = fields.Many2one(string='Publicador', comodel_name="secretary.publicadores")
     mes = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'), ], string='Mes', default=str(date.today().month))
     año = fields.Selection(get_years(), string='Año', default='2022')
     horas = fields.Integer(string='Horas', required=True)
     revisitas = fields.Integer(string="Revisitas")
     cursos = fields.Integer(string="Cursos Bíblicos")
     publicaciones = fields.Integer(string="Publicaciones")
     videos = fields.Integer(string="Videos")
     revisitas = fields.Integer(string="Revisitas")
     notas = fields.Text(string='Notas:')


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
