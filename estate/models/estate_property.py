from odoo import fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(string="Title",required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False,string="Selling Price")
    bedrooms = fields.Integer(default=2,string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('North', 'North'), ('South', 'South'), 
                   ('East', 'East'), ('West', 'West')],
        help = "Orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'),('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
        help = "State of the estate",
        required=True, copy=False, default="New"
    )
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer")
