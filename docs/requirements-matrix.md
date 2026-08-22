# Dayflow Requirements Matrix

| Flow requirement | Module |
|---|---|
| Employee profile/card | `dayflow_core` |
| Present/leave/absent indicators | `dayflow_attendance` + `dayflow_dashboard` |
| Resume/private information | `dayflow_core` |
| Skills/certifications | `dayflow_core` |
| PAN/UAN/employee code | `dayflow_core` |
| Bank details | `dayflow_core` |
| Department/job/manager/company/location | Odoo HR + `dayflow_core` |
| Employee cards view-only for employees | `dayflow_core` security/rules |
| Automatic employee/login ID | `dayflow_core` |
| HR/Admin creates employee | `dayflow_core` |
| Initial password/change later | Odoo users + HR workflow |
| Salary components | `dayflow_payroll` |
| Salary recalc from wage | `dayflow_payroll` |
| Salary HR/Admin only | `dayflow_payroll` security |
| Check-in/check-out | Odoo `hr_attendance` + `dayflow_attendance` |
| Work hours/extra hours | `dayflow_attendance` |
| Leave types | `dayflow_leave` |
| Leave approval | Odoo `hr_holidays` + `dayflow_leave` |
| Sick certificate | `dayflow_leave` |
| Attendance/leave -> payable days | `dayflow_payroll` |
