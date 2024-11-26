from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    has_catraca = fields.Boolean(string="Possui Catraca?")
    has_comanda = fields.Boolean(string="Possui Comanda?")
    pdv_version = fields.Char(string="Versão do PDV")
    # Exemplo de campo adicional
    custom_note = fields.Text(string="Nota Adicional")
