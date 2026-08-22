# Architecture

Odoo core remains the system of record.

dayflow_core
  ├── dayflow_attendance
  ├── dayflow_leave
  ├── dayflow_payroll
  ├── dayflow_dashboard
  └── dayflow_notifications

Keep employee, attendance and leave data in Odoo ORM. Payroll consumes approved HR data. Dashboard consumes controlled model methods.
