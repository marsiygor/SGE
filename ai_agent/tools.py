from langchain_core.tools import tool
from products.models import Product
from django.db.models import Sum, F

LOW_STOCK_THRESHOLD = 10


@tool
def check_product_stock(product_name: str) -> str:
    """Verifica a quantidade atual em estoque de um produto específico pelo nome."""
    if not product_name:
        return "Nome do produto não pode ser vazio."
    try:
        product = Product.objects.get(title__iexact=product_name)
        status = "CRÍTICO" if product.quantity < LOW_STOCK_THRESHOLD else "NORMAL"
        return f"Produto: {product.title} | Quantidade: {product.quantity} | Status: {status}"
    except Product.DoesNotExist:
        return f"Produto '{product_name}' não encontrado no sistema."
    except Exception as e:
        return f"Erro ao consultar estoque: {str(e)}"


@tool
def list_low_stock_products(threshold: int = LOW_STOCK_THRESHOLD) -> str:
    """Lista todos os produtos com estoque abaixo de um determinado limite."""
    try:
        low_stock_items = Product.objects.select_related('category').filter(quantity__lt=threshold).order_by('quantity')
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
        total_value = Product.objects.aggregate(
            total=Sum(F('quantity') * F('selling_price'))
        )['total'] or 0
        return f"O valor total do inventário é R$ {total_value:,.2f}"
    except Exception as e:
        return f"Erro ao calcular valor do inventário: {str(e)}"
