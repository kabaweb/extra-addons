import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create_task_for_won_lead(self):
        _logger.info("Iniciando criação de tarefa para a oportunidade: %s", self.name)

        # Buscando o projeto
        project = self.env['project.project'].search([('name', '=', 'CRM Services Project')], limit=1)
        if not project:
            _logger.error("Projeto 'CRM Services Project' não encontrado!")
            raise ValueError("Projeto 'CRM Services Project' não encontrado!")

        _logger.info("Projeto encontrado: %s (ID: %s)", project.name, project.id)

        # Criando uma tarefa
        task = self.env['project.task'].create({
            'name': f"Tarefa para Oportunidade: {self.name}",
            'project_id': project.id,
            'description': f"Descrição gerada automaticamente para a oportunidade {self.name}",
            'user_id': self.user_id.id,
        })

        _logger.info("Tarefa criada com sucesso: %s (ID: %s)", task.name, task.id)
