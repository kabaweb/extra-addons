from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_set_won_rainbowman(self):
        """Override the 'Set as Won' action to create a task in a specific project."""
        res = super(CrmLead, self).action_set_won_rainbowman()
        
        # Nome do projeto onde as tarefas serão criadas
        project_name = "Meu Projeto Padrão"  # Altere para o nome desejado
        
        # Buscar o projeto com base no nome
        project = self.env['project.project'].search([('name', '=', project_name)], limit=1)
        
        # Se o projeto não existir, cria automaticamente
        if not project:
            project = self.env['project.project'].create({
                'name': project_name,
            })

        # Cria uma tarefa para cada lead ganho
        for lead in self:
            self.env['project.task'].create({
                'name': f"Tarefa para o Lead {lead.name}",
                'project_id': project.id,
                'description': lead.description or 'Descrição do lead não fornecida.',
                'user_id': lead.user_id.id,  # Atribuir responsável do lead como responsável pela tarefa
                'partner_id': lead.partner_id.id,  # Relacionar a tarefa ao cliente
            })

        return res
