from django.db import models
from datetime import timedelta

class Commune(models.Model):
    nom = models.CharField(max_length=100)
    position = models.PositiveIntegerField(unique=True) # Zone 1 à 8

    class Meta:
        ordering = ['position']

    def __str__(self): return self.nom

class Gare(models.Model):
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    class Meta:
        ordering = ['commune__position', 'id']

    def __str__(self): return f"{self.nom} ({self.commune.nom})"

class Voyage(models.Model):
    SENS_CHOICES = [('ALLER', 'Anyama ➔ Port-Bouët'), ('RETOUR', 'Port-Bouët ➔ Anyama')]
    sens = models.CharField(max_length=10, choices=SENS_CHOICES)
    gare_depart_defaut = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='departs_v', null=True, blank=True)
    gare_arrivee_defaut = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='arrivees_v', null=True, blank=True)
    jour_depart = models.DateField()
    heure_depart = models.TimeField()
    est_ouvert = models.BooleanField(default=True)

    def get_heure_passage(self, gare_utilisateur):
        """Calcule le décalage basé sur 3 min par escale depuis le terminus"""
        toutes_gares = list(Gare.objects.all().order_by('commune__position', 'id'))
        try:
            index_gare = toutes_gares.index(gare_utilisateur)
        except (ValueError, TypeError):
            return timedelta(0)

        temps_par_escale = 3
        if self.sens == 'ALLER':
            minutes_decalage = index_gare * temps_par_escale
        else:
            minutes_decalage = (len(toutes_gares) - 1 - index_gare) * temps_par_escale
        return timedelta(minutes=minutes_decalage)

    def __str__(self): return f"{self.get_sens_display()} - {self.heure_depart}"

class Reservation(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    nom_passager = models.CharField(max_length=100)
    prenom_passager = models.CharField(max_length=100)
    gare_depart_nom = models.CharField(max_length=100)
    gare_arrivee_nom = models.CharField(max_length=100)
    code_ticket = models.CharField(max_length=20, unique=True)
    prix_paye = models.PositiveIntegerField()
    mode_paiement = models.CharField(max_length=20, null=True, blank=True)
    paye = models.BooleanField(default=False)
    # Champ pour stocker l'heure calculée au moment de la résa
    heure_reelle_passage = models.TimeField(null=True, blank=True)
    date_reservation = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    est_valide = models.BooleanField(default=True)
    date_utilisation = models.DateTimeField(null=True, blank=True)

    def __str__(self): return f"{self.code_ticket} - {self.nom_passager}"