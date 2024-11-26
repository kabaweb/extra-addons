{
    'name': 'CRM Serviços Opcional',
    'version': '16.0.1.0.0',
    'summary': 'Adiciona campos opcionais ao CRM para informações sobre recursos do sistema.',
    'description': """
        Este módulo adiciona campos opcionais ao CRM, permitindo registrar informações como:
        - Presença de catraca (sim ou não)
        - Uso de comanda (sim ou não)
        - Versão do PDV
        - Outros campos que podem ser configurados futuramente.
    """,
    'author': 'Edcarlos',
    'website': 'https://www.seusite.com',
    'category': 'CRM',
    'depends': ['crm'],
    'data': [
        'views/crm_servicos_opcional_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
