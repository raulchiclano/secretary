# -*- coding: utf-8 -*-

from email.policy import default
import string
from odoo import models, fields, api
from datetime import *


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
    #id = fields.Integer(string= 'ID', default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))


class informes(models.Model):
     _name = 'secretary.informes'
     _description = 'Informe de predicación'
     
     #current_year = fields.Integer(string="Año actual", default=datetime.now().year)
     #current_year = str(current_year)

     
     nombre = fields.Many2one(string='Publicador', comodel_name="secretary.publicadores")
     mes = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'), ], string='Mes', default=str(date.today().month))
     current_year = datetime.strftime(datetime.today(),'%Y')
     año = fields.Selection(get_years(), string='Año', default=current_year)
     horas = fields.Integer(string='Horas', required=True)
     revisitas = fields.Integer(string="Revisitas")
     cursos = fields.Integer(string="Cursos Bíblicos")
     publicaciones = fields.Integer(string="Publicaciones")
     videos = fields.Integer(string="Videos")
     revisitas = fields.Integer(string="Revisitas")
     notas = fields.Text(string='Notas:')


def g_create(self):
    grupo = {
        'name': 'caca' 
    }
    self.env['secretary.grupos'].create(grupo)
