/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DayflowDashboard extends Component {
    static template = "dayflow_dashboard.Dashboard";
}

registry.category("actions").add("dayflow_dashboard", DayflowDashboard);
