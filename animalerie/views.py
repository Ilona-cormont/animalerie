from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Equipement
from .forms import MoveForm
from django.contrib import messages
from django.shortcuts import render, redirect 
from .forms import *
# Create your views here.


def post_list(request):
    animal = Animal.objects.filter()
    equipement = Equipement.objects.all()
    return render(request, 'animalerie/post_list.html', {'equipement': equipement, 'animals': animal})


def equipement_list(request):
    equipement = Equipement.objects.all()
    return render(request, 'animalerie/equipement_list.html', {'equipement': equipement})


def post_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    lieu = animal.lieu
    form = MoveForm()
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Mangeoire" and animal.etat=='Affamé':
                animal.etat="Repus"
                animal.save()
                nouveau_lieu.disponibilite="Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Votre animal a bien été déplacé dans la mangeoire')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Roue" and animal.etat=='Repus':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Fatigué"
                animal.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Votre animal a bien été déplacé dans la roue')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Nid" and animal.etat=='Fatigué':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Endormi"
                animal.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Votre animal a bien été déplacé dans le nid')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Litière" and animal.etat=='Endormi':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Affamé"
                animal.save()
                nouveau_lieu.disponibilite = "Libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Votre animal a bien été déplacé dans la litière')
            else :
                print('message')
                messages.add_message(request, messages.INFO, 'Désolé, vous ne pouvez pas déplacer cet animal à cet endroit.')
        return redirect('post_detail', pk=pk)
    else:
        form = MoveForm()
        return render(request,
                    'animalerie/post_detail.html',
                    {'animal': animal, 'lieu': lieu, 'form': form})


  
def ajout_animal(request): 
    form = AddForm()
    if request.method == 'POST': 
        form = AddForm(request.POST, request.FILES) 
        if form.is_valid(): 
            form.save() 
            messages.add_message(request, messages.INFO, 'Votre animal a bien été ajouté ! ')
            return redirect('ajout_animal') 
    else: 
        form = AddForm() 
    return render(request, 'animalerie/ajout_animal.html', {'form' : form}) 
