from odoo import api, fields, models
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
    property_type_id= fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area", compute="_total_area")
    best_price = fields.Float(required=True, compute="_calculate_best_price")
    
    @api.depends('living_area','garden_area')
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area
            
    @api.depends('offer_ids')
    def _calculate_best_price(self):
        for record in self:
            record.best_price = 0
            for offer in record.offer_ids:
                if offer.price > record.best_price:
                    record.best_price = offer.price


    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden==True:
            self.garden_area = 10
            self.garden_orientation="North"
        else:
            self.garden_area = 0
            self.garden_orientation=""
            
    def action_sold(self):
        for record in self:
            if record.state=="Canceled":
                raise UserError("Canceled properties cannot be sold")
            else:
                record.state="Sold"    
            
    def action_cancel(self):
        for record in self:
            if record.state=="Sold":
                raise UserError("Sold properties cannot be canceled")
            else:
                record.state="Canceled"  