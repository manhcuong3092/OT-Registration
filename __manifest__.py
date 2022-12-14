{
    'name': "OT Registration",
    'summary': """Odoo OT Registration module""",
    'description': """Managing OT request""",
    'author': "Cuong",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'hr',
        'project'
    ],
    'data': [
        "security/ir.model.access.csv",
        'security/ot_security.xml',
        'views/ot_registration_view.xml',
        'views/ot_request_line_view.xml',
        'data/mail_template.xml',
        'data/data.xml'
    ],
    'installable': True,
    'application': True,
}
