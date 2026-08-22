{
    "name": "Dayflow Payroll",
    "version": "1.0.0",
    "summary": "Dayflow salary and payroll calculation",
    "category": "Human Resources",
    "license": "LGPL-3",
    "depends": ["dayflow_core", "dayflow_attendance", "dayflow_leave"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/salary_views.xml",
        "views/payroll_views.xml",
        "views/menus.xml"
    ],
    "installable": true
}
