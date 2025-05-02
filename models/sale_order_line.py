from odoo import api, models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    def _get_computed_taxes(self):
        self.ensure_one()
        
        # Obtener los impuestos calculados por la implementación estándar
        tax_ids = super()._get_computed_taxes()
        
        # Solo agregar percepciones para documentos de venta
        if self.move_id.is_sale_document(include_receipts=True) and self.move_id.partner_id.perceptions:
            company_domain = self.env['account.tax']._check_company_domain(self.move_id.company_id)
            perception_taxes = self.move_id.partner_id.perceptions.filtered_domain(company_domain)
            
            if perception_taxes:
                # Filtrar por compañía si no lo hizo el método padre
                if self.company_id:
                    perception_taxes = perception_taxes._filter_taxes_by_company(self.company_id)
                
                # Combinar con los impuestos existentes
                tax_ids = tax_ids + perception_taxes if tax_ids else perception_taxes
        
        return tax_ids
   