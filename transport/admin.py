from django.contrib import admin
from django import forms
from .models import Voyage, Gare, Commune


# --- FORMULAIRE ÉPURÉ ---
class VoyageForm(forms.ModelForm):
    class Meta:
        model = Voyage
        # On ne garde que les champs dont l'admin a réellement besoin
        fields = ['sens', 'jour_depart', 'heure_depart', 'est_ouvert']
        widgets = {
            'heure_depart': forms.TimeInput(attrs={'type': 'time', 'step': '300'}),
        }


@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    form = VoyageForm
    list_display = ('id', 'sens', 'jour_depart', 'heure_depart', 'est_ouvert')
    list_filter = ('sens', 'jour_depart', 'est_ouvert')

    def save_model(self, request, obj, form, change):
        """
        Logique automatique : remplit les gares terminus selon le sens choisi
        """
        # On récupère toutes les gares triées par la position de leur commune
        gares = Gare.objects.select_related('commune').order_by('commune__position')

        if gares.exists():
            gare_anyama = gares.first()  # La plus petite position (Anyama)
            gare_port_bouet = gares.last()  # La plus grande position (Port-Bouët)

            if obj.sens == 'ALLER':
                obj.gare_depart_defaut = gare_anyama
                obj.gare_arrivee_defaut = gare_port_bouet
            elif obj.sens == 'RETOUR':
                obj.gare_depart_defaut = gare_port_bouet
                obj.gare_arrivee_defaut = gare_anyama

        super().save_model(request, obj, form, change)


# --- STRUCTURE DU RÉSEAU ---
@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ('nom', 'commune')


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'position')