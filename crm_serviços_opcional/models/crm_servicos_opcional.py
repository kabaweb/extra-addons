from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    has_catraca = fields.Boolean(string="Possui Catraca?")
    has_comanda = fields.Boolean(string="Possui Comanda?")
    pdv_version = fields.Char(string="Versão do PDV")
    custom_note = fields.Text(string="Nota Adicional")

    def write(self, vals):
        # Verificar se o lead está mudando para o estágio "Won"
        if 'stage_id' in vals:
            won_stage = self.env.ref('crm.stage_lead2')  # Substitua pelo XML ID correto do estágio "Won"
            if isinstance(vals['stage_id'], int) and vals['stage_id'] == won_stage.id:
                for lead in self:
                    # Criar a tarefa no projeto desejado
                    project_id = self.env['project.project'].search([('name', '=', 'CRM Tasks')], limit=1)
                    if not project_id:
                        project_id = self.env['project.project'].create({'name': 'CRM Tasks'})

                    self.env['project.task'].create({
                        'name': f'Tarefa para Lead: {lead.name}',
                        'project_id': project_id.id,
                        'description': f'Tarefa criada automaticamente para o lead "{lead.name}".',
                        'user_id': lead.user_id.id,  # Atribui ao vendedor responsável pelo lead
                    })

        return super(CrmLead, self).write(vals)
