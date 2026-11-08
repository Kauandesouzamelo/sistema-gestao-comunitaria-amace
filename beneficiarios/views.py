
from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiario
from .forms import BeneficiarioForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('beneficiarios.view_beneficiario', raise_exception=True)
def listar_beneficiarios(request):
    beneficiarios = Beneficiario.objects.all()

    return render(request, 'beneficiarios/listar.html', {
        'beneficiarios': beneficiarios
    })


@login_required
@permission_required('beneficiarios.add_beneficiario', raise_exception=True)
def cadastrar_beneficiario(request):

    if request.method == 'POST':
        form = BeneficiarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_beneficiarios')

    else:
        form = BeneficiarioForm()

    return render(request, 'beneficiarios/cadastrar.html', {
        'form': form
    })


@login_required
@permission_required('beneficiarios.change_beneficiario', raise_exception=True)
def editar_beneficiario(request, pk):
    beneficiario = get_object_or_404(Beneficiario, pk=pk)

    if request.method == "POST":
        form = BeneficiarioForm(request.POST, instance=beneficiario)

        if form.is_valid():
            form.save()
            return redirect("listar_beneficiarios")
    else:
        form = BeneficiarioForm(instance=beneficiario)

    return render(
        request,
        "beneficiarios/cadastrar.html",
        {"form": form}
    )


@login_required
@permission_required('beneficiarios.delete_beneficiario', raise_exception=True)
def excluir_beneficiario(request, pk):
    beneficiario = get_object_or_404(Beneficiario, pk=pk)

    if request.method == "POST":
        beneficiario.delete()
        return redirect("listar_beneficiarios")

    return render(
        request,
        "beneficiarios/confirmar_exclusao.html",
        {"beneficiario": beneficiario}
    )
