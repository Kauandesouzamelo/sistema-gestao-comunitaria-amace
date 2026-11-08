from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ItemDoacao
from .forms import ItemDoacaoForm
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import MovimentacaoEstoque
from .forms import MovimentacaoEstoqueForm
from django.db.models import Sum, Count
from beneficiarios.models import Beneficiario
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('controle_estoque.view_itemdoacao', raise_exception=True)
def listar_produtos(request):
    produtos = ItemDoacao.objects.all()

    return render(
        request,
        'controle_estoque/listar.html',
        {'produtos': produtos}
    )


@login_required
@permission_required('controle_estoque.add_itemdoacao', raise_exception=True)
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ItemDoacaoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ItemDoacaoForm()

    return render(
        request,
        'controle_estoque/cadastrar.html',
        {'form': form}
    )


@login_required
@permission_required('controle_estoque.add_movimentacaoestoque', raise_exception=True)
def registrar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)

        if form.is_valid():
            movimentacao = form.save(commit=False)

            if movimentacao.quantidade <= 0:
                form.add_error(
                    'quantidade', 'Informe uma quantidade maior que zero.')

            elif movimentacao.tipo == 'saida' and not movimentacao.beneficiario:
                form.add_error(
                    'beneficiario', 'Selecione o beneficiário da saída.')

            else:
                with transaction.atomic():
                    item = ItemDoacao.objects.select_for_update().get(
                        pk=movimentacao.item.pk
                    )

                    if movimentacao.tipo == 'saida':
                        if movimentacao.quantidade > item.quantidade_estoque:
                            form.add_error(
                                'quantidade',
                                'Estoque insuficiente para esta saída.'
                            )
                        else:
                            item.quantidade_estoque -= movimentacao.quantidade

                    else:
                        item.quantidade_estoque += movimentacao.quantidade

                    if not form.errors:
                        item.save()
                        movimentacao.save()
                        return redirect('listar_produtos')
    else:
        form = MovimentacaoEstoqueForm()

    return render(
        request,
        'controle_estoque/movimentar.html',
        {'form': form}
    )


@login_required
@permission_required('controle_estoque.view_movimentacaoestoque', raise_exception=True)
def historico_movimentacoes(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related(
        'item',
        'beneficiario'
    ).all()

    return render(
        request,
        'controle_estoque/historico.html',
        {'movimentacoes': movimentacoes}
    )


@login_required
@permission_required('controle_estoque.view_movimentacaoestoque', raise_exception=True)
def relatorios(request):

    total_beneficiarios = Beneficiario.objects.filter(
        status='ativo'
    ).count()

    total_produtos = ItemDoacao.objects.count()

    total_estoque = ItemDoacao.objects.aggregate(
        total=Sum('quantidade_estoque')
    )['total'] or 0

    total_entradas = MovimentacaoEstoque.objects.filter(
        tipo='entrada'
    ).aggregate(total=Sum('quantidade'))['total'] or 0

    total_saidas = MovimentacaoEstoque.objects.filter(
        tipo='saida'
    ).aggregate(total=Sum('quantidade'))['total'] or 0

    contexto = {
        'total_beneficiarios': total_beneficiarios,
        'total_produtos': total_produtos,
        'total_estoque': total_estoque,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
    }

    return render(
        request,
        'controle_estoque/relatorios.html',
        contexto
    )
