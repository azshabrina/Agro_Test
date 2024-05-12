odoo.define("dashboard_dashboard.DashboardDashboard", function (require) {
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var web_client = require('web.web_client');
   var session = require('web.session');
   var ajax = require('web.ajax');
   var _t = core._t;
   var rpc = require('web.rpc');
   var self = this;
   var currency;
   var DashBoard = AbstractAction.extend({
       contentTemplate: 'DashboardDashboard',
init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['MainSection'];
       },
       start: function() {
           var self = this;
           this.set("title", 'Dashboard');
           return this._super().then(function() {
               self.render_dashboards();
           });
       },
       willStart: function(){
           var self = this;
           return this._super()
       },
       render_dashboards: function() {
           var self = this;
           this.fetch_data_so()
           this.fetch_data_po()
           var templates = []
           var templates = ['MainSection'];
           _.each(templates, function(template) {
               self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
           });
       },
       fetch_data_so: function() {
           var self = this
//          fetch data to the tiles
           var def1 = this._rpc({
               model: 'sale.order',
               method: "get_data",
           })
           .then(function (result) {
            const rupiah = (number)=>{
                            return new Intl.NumberFormat("id-ID", {
                              style: "currency",
                              currency: "IDR"
                            }).format(number);
                          }

                var total_order_amount_idr = rupiah(result.total_order_amount);
               $('#total_order').append('<span>' + result.total_order + '</span>');
               $('#total_order_amount').append('<span>' + total_order_amount_idr + '</span>');
               $('#total_quotation').append('<span>' + result.total_quotation + '</span>');
               $('#total_customer').append('<span>' + result.total_customer + '</span>');
           });
               return $.when(def1);
       },
       fetch_data_po: function() {
           var self = this
//          fetch data to the tiles
           var def1 = this._rpc({
               model: 'purchase.order',
               method: "get_data",
           })
           .then(function (result) {
            const rupiah = (number)=>{
                            return new Intl.NumberFormat("id-ID", {
                              style: "currency",
                              currency: "IDR"
                            }).format(number);
                          }

                var total_purchase_amount_idr = rupiah(result.total_purchase_amount);
               $('#total_purchase').append('<span>' + result.total_purchase + '</span>');
               $('#total_purchase_amount').append('<span>' + total_purchase_amount_idr + '</span>');
               $('#total_priority').append('<span>' + result.total_priority + '</span>');
               $('#total_supplier').append('<span>' + result.total_supplier + '</span>');
           });
               return $.when(def1);
       },
       goBackend(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Purchase Order'),
            res_model: 'sale.order',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            target: 'self',
            domain: [['state', 'not in', ['sale','done','cancel']]],
        });
    },
   });
   core.action_registry.add('custom_dashboard', DashBoard);
   return DashBoard;
});