# -*- coding: utf-8 -*-

# Para ver print() en los logs en Docker
import logging
     
_logger = logging.getLogger(__name__)
_logger.info('Mensaje')
# ----------------------------------------


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
     activo = fields.Boolean(string='Activo', default='True', readonly=True)
     informe_id = fields.One2many("secretary.informes", "nombre", string="Mis Informes")





     def f_activo(self):
        self.activo = not self.activo




class grupos(models.Model):
    _name = 'secretary.grupos'
    _description = 'Grupos de Servicio'

    id = fields.Integer(string= 'Nombre', default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    name = fields.Integer(string='Nombre', related="id")


    def g_create(self):
       grupo = {
           'name': 'Grupo'
       }
       print(grupo)
       self.env['secretary.grupos'].create(grupo) 


class informes(models.Model):
     _name = 'secretary.informes'
     _description = 'Informe de predicación'
     _rec_name = 'fecha'
     
     #current_year = fields.Integer(string="Año actual", default=datetime.now().year)
     #current_year = str(current_year)

     
     nombre = fields.Many2one("secretary.publicadores", string='Publicador')
     mes = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'), ], string='Mes', default=str(date.today().month))
     current_year = datetime.strftime(datetime.today(),'%Y')
     fecha = fields.Char(compute="_compute_date", store=True)
     año = fields.Selection(get_years(), string='Año', default=current_year)
     horas = fields.Integer(string='Horas', required=True)
     revisitas = fields.Integer(string="Revisitas")
     cursos = fields.Integer(string="Cursos Bíblicos")
     publicaciones = fields.Integer(string="Publicaciones")
     videos = fields.Integer(string="Videos")
     revisitas = fields.Integer(string="Revisitas")
     notas = fields.Text(string='Notas:')

     @api.depends("mes")
     def _compute_date(self):
        for record in self:
            record.fecha = "%s-%s" %(record.mes,record.año)


     def fechas(self):
        informes = self.env['secretary.informes'].search([])
        fechas_filtered = informes.filtered(lambda f: f.año == '2022')
        self.date(fechas_filtered)

     def date(self, informes):
        fecha = []
        for fechas in informes:
            fecha.append((fechas.fecha, fechas.fecha))
        fecha = list(dict.fromkeys(fecha))
        fecha.sort(reverse=True)
        print(fecha, flush=True)




     _sql_constraints = [
        ('nombre_unique', 'unique(nombre, mes, año)', '¡Solo puede introducir un informe por publicador!')
    ]

    


class totales(models.Model):
    _name = 'secretary.totales'
    _description = 'Totales de la predicación'
    _auto = False
    _rec_name = 'id'

    def _compute_date(self):
        informes = self.env['secretary.informes'].search([])
        fechas_filtered = informes.filtered(lambda f: f.año == '2022')
        fecha = []
        for fechas in fechas_filtered:
            fecha.append((fechas.fecha, fechas.fecha))
        fecha = list(dict.fromkeys(fecha))
        fecha.sort(reverse=True)
        #print(fecha, flush=True)
        return fecha

    def date(self, informes):
        fecha = []
        for fechas in informes:
            fecha.append((fechas.fecha, fechas.fecha))
        fecha = list(dict.fromkeys(fecha))
        fecha.sort(reverse=True)
        #print(fecha, flush=True)
        return fecha
    #base = fields.Many2one("secretary.informes") # Escoger el campo Fecha sin repetir
    fecha = fields.Selection(_compute_date, string = 'Escoga un mes para auditar')
    




 












class InformesReport(models.AbstractModel):
    _name='report.secretary.informe_mensual'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('secretary.informe_mensual')
        return {
            'doc_ids': docids,
            'doc_model': self.env['secretary.tarjeta_publicador'],
            'docs': self.env['secretary.publicadores'].browse(docids)
        }





