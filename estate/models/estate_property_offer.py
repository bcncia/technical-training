from odoo import api, fields, models
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Model"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False
    )
    partner_id= fields.Many2one("res.partner", string="Partner",required=True)
    property_id= fields.Many2one("estate.property", string="Property",required=True)
    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(string="Deadline",compute="_compute_deadline", inverse="_inverse_compute_days")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline =  fields.Date.today() + timedelta(days=record.validity) 

    def _inverse_compute_days(self):
        for record in self:
             if record.create_date:
                 record.validity = abs((record.date_deadline - fields.Date.today()).days)
             else:    
                record.validity = abs((record.date_deadline - record.create_date.date()).days)
            
            