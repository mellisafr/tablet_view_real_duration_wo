# File: __manifest__.py
# Module: tablet_view_real_duration_wo

{
    'name': 'MRP Workorder Real-Time Duration',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Real-time duration tracking for work orders even when tablet view is closed',
    'description': """
        This module keeps work order real duration running in real-time even when
        tablet view is closed. Timer will continue running in background until
        user clicks Pause/Done button.
        
        Features:
        - Real-time duration calculation
        - Duration keeps updating even when view is closed
        - Timer only stops when manually paused
    """,
    'author': 'Mellisa FR',
    'website': 'https://www.linkedin.com/in/mellisafr/',
    'depends': ['mrp', 'mrp_workorder'],
    'data': [
        'views/mrp_workorder_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'
}