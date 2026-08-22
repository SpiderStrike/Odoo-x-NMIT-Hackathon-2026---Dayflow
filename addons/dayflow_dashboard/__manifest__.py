{
    "name": "Dayflow Dashboard",
    "version": "1.0.0",
    "summary": "Dayflow HR and employee dashboard",
    "category": "Human Resources",
    "license": "LGPL-3",
    "depends": ["dayflow_core", "dayflow_attendance", "dayflow_leave", "dayflow_payroll"],
    "data": ["views/dashboard_views.xml", "views/menus.xml"],
    "assets": {
        "web.assets_backend": [
            "dayflow_dashboard/static/src/js/dashboard.js",
            "dayflow_dashboard/static/src/xml/dashboard.xml",
            "dayflow_dashboard/static/src/scss/dashboard.scss"
        ]
    },
    "installable": true
}
