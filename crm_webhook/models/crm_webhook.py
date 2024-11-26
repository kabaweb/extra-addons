import requests
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def send_to_webhook(self):
        """Envia informações detalhadas do lead para o webhook ao marcar como 'Ganho'."""
        webhook_url = "https://webhooks.n8nsip.bmhelp.click/webhook/f03821b7-da20-4fdc-8571-e92de27e1a1a"

        for record in self:
            # Dados principais do lead
            lead_data = {
                "lead_name": record.name,
                "lead_description": record.description or "",
                "expected_revenue": record.expected_revenue,
                "probability": record.probability,
                "stage": record.stage_id.name,
                "status": "Ganho" if record.stage_id.is_won else "Perdido" if record.stage_id.is_lost else "Aberto",
                "create_date": record.create_date.strftime('%Y-%m-%d %H:%M:%S') if record.create_date else None,
                "write_date": record.write_date.strftime('%Y-%m-%d %H:%M:%S') if record.write_date else None,
            }

            # Dados do cliente (parceiro relacionado)
            partner_data = {
                "customer_name": record.partner_id.name if record.partner_id else None,
                "customer_email": record.partner_id.email if record.partner_id else None,
                "customer_phone": record.partner_id.phone if record.partner_id else None,
                "customer_mobile": record.partner_id.mobile if record.partner_id else None,
                "customer_website": record.partner_id.website if record.partner_id else None,
                "customer_address": {
                    "street": record.partner_id.street or "",
                    "city": record.partner_id.city or "",
                    "state": record.partner_id.state_id.name if record.partner_id.state_id else "",
                    "country": record.partner_id.country_id.name if record.partner_id.country_id else "",
                    "zip": record.partner_id.zip or "",
                } if record.partner_id else None,
            }

            # Dados do vendedor e da equipe de vendas
            sales_data = {
                "salesperson": record.user_id.name if record.user_id else None,
                "sales_team": record.team_id.name if record.team_id else None,
            }

            # Dados de atividades
            activity_data = {
                "open_activities": len(record.activity_ids),
                "closed_activities": len(record.activity_ids.filtered(lambda a: a.date_deadline and a.date_deadline < fields.Date.today())),
            }

            # Monta o payload completo
            payload = {
                "lead_data": lead_data,
                "partner_data": partner_data,
                "sales_data": sales_data,
                "activity_data": activity_data,
            }

            try:
                # Envia os dados para o webhook
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()  # Lança erro se o status não for 200
                record.message_post(body="Dados enviados ao webhook com sucesso.")
            except requests.exceptions.RequestException as e:
                # Registra o erro no chatter
                record.message_post(body=f"Erro ao enviar dados ao webhook: {e}")
