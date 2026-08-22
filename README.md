# Dayflow — Odoo x NMIT Hackathon 2026

Dayflow is an Odoo-based Human Resource Management System built around the hackathon flow.

## Scope

The implementation is organized around the required HR flow:

1. Employee management and profiles
2. Automatic employee/login ID generation
3. Role-based access and view-only employee cards
4. Attendance: check-in/check-out, work hours and status
5. Leave: Paid Time Off, Sick Leave and Unpaid Leave
6. Leave approval and medical-certificate attachment
7. Salary component calculation
8. Attendance/leave-driven payable days
9. Payroll/net salary calculation
10. HR/Admin dashboard and employee self-service

## Modules

- `dayflow_core` — employee data, ID generation, roles, profile fields
- `dayflow_attendance` — attendance and present/absent/leave status
- `dayflow_leave` — leave types, requests, approvals and attachments
- `dayflow_payroll` — salary structure, payable days and payroll
- `dayflow_dashboard` — role-specific HR/employee dashboard
- `dayflow_notifications` — reusable notification model

## Team split

| Member | Branch | Responsibility |
|---|---|---|
| Member 1 | `feature/employee` | Core employee, users, ID generation, security |
| Member 2 | `feature/attendance` | Check-in/out, work hours, status, dashboard KPIs |
| Member 3 | `feature/leave` | Leave types, approval, sick-leave attachment |
| Member 4 | `feature/payroll` | Salary formulas, payable days, payroll |

`main` should only receive tested pull requests.

## Odoo

The scaffold targets Odoo 18 conventions and uses Odoo Community HR modules where possible. If the hackathon environment uses a different Odoo version, validate view/model API differences before deployment.
