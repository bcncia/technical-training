from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag Model"

    name = fields.Char(string="Name",required=True)