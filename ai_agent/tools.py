from langchain_core.tools import tool
from products.models import Product


@tool
def check_product_stock(product_name: str) -> str:
    """Verifica a quantidade atual em estoque de um produto específico pelo nome."""
    try:
        product = Product.objects.filter(title__icontains=product_name).first()
        if not product:
            return f"Produto '{product_name}' não encontrado no sistema."
        status = "CRÍTICO" if product.quantity < 10 else "NORMAL"
        return f"Produto: {product.title} | Quantidade: {product.quantity} | Status: {status}"
    except Exception as e:
        return f"Erro ao consultar estoque: {str(e)}"


@tool
def list_low_stock_products(threshold: int = 10) -> str:
    """Lista todos os produtos com estoque abaixo de um determinado limite."""
    try:
        low_stock_items = Product.objects.filter(quantity__lt=threshold).order_by('quantity')
        if not low_stock_items.exists():
            return f"Não há produtos com estoque abaixo de {threshold} unidades."
        report_lines = [f"--- Relatório de Estoque Crítico (< {threshold} un.) ---"]
        for prod in low_stock_items:
            cat_name = prod.category.name if prod.category else 'N/A'
            report_lines.append(f"- {prod.title}: {prod.quantity} un. (Cat: {cat_name})")
        return "\n".join(report_lines)
    except Exception as e:
        return f"Erro ao gerar relatório de estoque: {str(e)}"


@tool
def get_total_inventory_value() -> str:
    """Calcula o valor total monetário do estoque atual (quantidade * preço de venda)."""
    try:
        products = Product.objects.all()
        total_value = sum(p.quantity * p.selling_price for p in products if p.selling_price)
        return f"O valor total do inventário é R$ {total_value:,.2f}"
    except Exception as e:
        return f"Erro ao calcular valor do inventário: {str(e)}"
