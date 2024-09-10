from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Model"

    price = fields.Float()
    status = fields.Selection(
        string='State',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False, default="New"
    )
    partner_id= fields.Many2one("res.partner", string="Partner",required=True)
    property_id= fields.Many2one("estate.property", string="Property",required=True)