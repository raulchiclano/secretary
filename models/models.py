# -*- coding: utf-8 -*-

# Para ver print() en los logs en Docker
#import logging
#rom select import select

#_logger = logging.getLogger(__name__)
#_logger.info('Mensaje')
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
     tipo_publicador = fields.Selection(string= "Tipo de publicador", related='nombre.tipo')
     mes = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'), ], string='Mes', default=lambda self: str((date.today().month)-1))
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
     este_mes_aux = fields.Boolean(string = "Aux. 30/50 horas", readonly=True) #TODO: Integrarlo cuadno se filtre campos para mayor comodida y estetica
     tipo_informe = fields.Selection([('P','Publicador'), ('A', 'Auxiliar'), ('R','Regular')], string= "Tipo de Informe", default='P')

     def este_mes_aux_activo(self):
        self.este_mes_aux = not self.este_mes_aux     

     @api.depends("mes")
     def _compute_date(self):
        for record in self:
            record.fecha = "%s-%s" %(record.mes,record.año)

     @api.onchange('nombre')
     def _set_tipo_informe(self):
        print("Toc,toc", self.nombre.tipo, flush=True)
        if self.nombre.tipo != False:
            self.tipo_informe = "%s" %(self.nombre.tipo)
        else:
            pass

    # AGRUPACION DE TOTALES SUMADOS PARA EL REPORTE "TOTALES MENSUALES"
     def get_sum_totales_mensuales(self):
        grouped = self.env['secretary.informes'].read_group(
            [('fecha', '=', self.fecha),],# WHERE
            [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], # FUNCTION IN SELECT; SELECT SUM (cv) AS total
            ['tipo_informe'] # GROUPBY
        )
        return grouped # devuelve array de tuplas      

     



     _sql_constraints = [
        ('nombre_unique', 'unique(nombre, mes, año)', '¡Solo puede introducir un informe por publicador!')
    ]




class TotalesMensuales(models.TransientModel):
    _name = 'secretary.test_report'
    _description = 'Totales mensuales de la predicación'
   # _inherit = 'secretary.informes'
   # _auto = False
   # _rec_name = 'id'

   
    def _informe_sort(self):
        informes = self.env['secretary.informes'].search([])
        informes_sorted = informes.sorted(key= lambda i : i.fecha ,reverse=True)
        menu_fecha = []
        for informe in informes_sorted:
            menu_fecha.append((informe.fecha, informe.fecha))
        menu_fecha = list(dict.fromkeys(menu_fecha))
        return menu_fecha

    mes_seleccionado = fields.Selection(_informe_sort, string = "Escoga mes para generar informe", required = True)
    
    def print_report_test(self):
        '''grouped = self.env['secretary.informes'].read_group(
            [('fecha', '=', self.mes_seleccionado),],# WHERE
            [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], # FUNCTION IN SELECT; SELECT SUM (cv) AS total
            ['tipo_informe'] # GROUPBY
        )'''
        data = {
            'mes_seleccionado': self.mes_seleccionado,
        }
        return self.env.ref('secretary.action_test_report').report_action(self)

    def get_sum_totales_mensuales(self):
        grouped = self.env['secretary.informes'].read_group(
            [('fecha', '=', self.mes_seleccionado),],# WHERE
            [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], # FUNCTION IN SELECT; SELECT SUM (cv) AS total
            ['tipo_informe'] # GROUPBY
        )
        print(grouped, flush=True)
        return grouped # devuelve array de tuplas


    



#Extras para probar cosas:
'''
    def sumar_horas(self):
        print("Hasta aquí el boton funciona",self.mes_seleccionado ,flush=True)
        total_informes = self.env['secretary.informes'].search([])
        total_informes_filtered = total_informes.filtered(lambda i : i.fecha == self.mes_seleccionado)
        for informe in total_informes_filtered:
            print(informe.tipo_publicador, flush=True)
        
    # AGRUPACIÓN (read_group) COPIADA A INFORME | TODO: EN DESUSO
    
    
    def _compute_horas(self):
        select_fecha = self.mes_seleccionado
        print("Debug: esto es select_fechas:  ",select_fecha, flush=True)
        total_informes = self.env['secretary.informes'].search(['fecha','=','self.mes_seleccionado'])
        total_informes_mapped = total_informes.mapped('horas')
        total_horas = 0
        for horas in total_informes_mapped:
            total_horas = total_horas + horas
        self.t_horas = total_horas
        print("Las horas son:",total_horas, flush=True)
'''


 
# MODELO PARA REPORTE TARJETA DE PUBLICADORES       
class InformesReport(models.AbstractModel):
    _name='report.secretary.informe_mensual'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('secretary.report_tarjeta_publicador')
        return {
            'doc_ids': docids,
            'doc_model': self.env['secretary.publicadores'],
            'docs': self.env['secretary.publicadores'].browse(docids)
        }




