from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    has_catraca = fields.Boolean(string="Possui Catraca?")
    has_comanda = fields.Boolean(string="Possui Comanda?")
    pdv_version = fields.Char(string="Versão do PDV")
    custom_note = fields.Text(string="Nota Adicional")

    def write(self, vals):
        # Identificar se o estágio foi alterado para "Won"
        if 'stage_id' in vals:
            won_stage = self.env.ref('crm.stage_lead2')  # Substitua pelo XML ID correto do estágio "Won"
            if isinstance(vals['stage_id'], int) and vals['stage_id'] == won_stage.id:
                for lead in self:
                    # Verifique se um projeto específico está definido
                    project = self.env['project.project'].search([('name', '=', 'CRM Services Project')], limit=1)
                    
                    if not project:
                        # Crie o projeto se ele não existir
                        project = self.env['project.project'].create({'name': 'CRM Services Project'})

                    # Criar a tarefa no projeto
                    self.env['project.task'].create({
                        'name': f'Tarefa para Lead: {lead.name}',
                        'project_id': project.id,
                        'description': f'Tarefa criada automaticamente para o lead "{lead.name}".',
                        'user_id': lead.user_id.id,  # Responsável: vendedor do lead
                    })

        return super(CrmLead, self).write(vals)
