import requests
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def send_to_webhook(self):
        """Envia informações do lead para o webhook quando marcado como 'Ganho'."""
        webhook_url = "https://editor.n8nsip.bmhelp.click/webhook-test/f03821b7-da20-4fdc-8571-e92de27e1a1a"

        for record in self:
            # Dados do lead a serem enviados
            payload = {
                "lead_name": record.name,
                "customer": record.partner_id.name if record.partner_id else None,
                "expected_revenue": record.expected_revenue,
                "stage": record.stage_id.name,
                "email": record.partner_id.email if record.partner_id and record.partner_id.email else None,
            }

            try:
                # Envia os dados para o webhook
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()  # Lança erro se o status não for 200
                # Registra o sucesso no chatter
                record.message_post(body="Dados enviados ao webhook com sucesso.")
            except requests.exceptions.RequestException as e:
                # Registra o erro no chatter
                record.message_post(body=f"Erro ao enviar dados ao webhook: {e}")

    def write(self, vals):
        """Intercepta mudanças no estágio e verifica se é 'Ganho'."""
        res = super(CrmLead, self).write(vals)

        # Obtém o estágio "Ganho"
        stage_won = self.env.ref('crm.stage_lead4')  # Certifique-se de usar o ID correto do estágio "Ganho"

        if 'stage_id' in vals:
            for record in self:
                if record.stage_id == stage_won:
                    record.send_to_webhook()

        return res
