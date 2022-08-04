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
        'views/ot_registration_view.xml'
    ],
    'installable': True,
    'application': True,
}
