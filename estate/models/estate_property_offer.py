from odoo import api, fields, models

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
    validity = fields.Integer(string="Validity (days)",default=7,compute="_compute_deadline", inverse="_inverse_compute_days")
    date_deadline = fields.Date(string="Deadline")

    @api.depends("date_deadline")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + record.validity

    def _inverse_compute_days(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date)
            