from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Voyage, Gare, Reservation
from datetime import date, datetime, timedelta
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# Sécurité et Authentification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm


# --- VUES UTILISATEURS (CLIENTS) ---

def accueil(request):
    """
    Affichage des départs.
    - Home : Heure brute admin.
    - Recherche : Heure calculée selon la gare de départ[cite: 5].
    """
    gares = Gare.objects.all().order_by('commune__position')

    gare_dep_id = request.GET.get('depart')
    gare_arr_id = request.GET.get('arrivee')

    now_dt = datetime.now()
    heure_actuelle = now_dt.time()
    limite_visibilite = (now_dt - timedelta(minutes=10)).time()

    # 1. CAS DE RECHERCHE ACTIVE (Calcul de l'heure approximative)
    if gare_dep_id and gare_arr_id:
        try:
            g_dep = Gare.objects.get(id=gare_dep_id)
            g_arr = Gare.objects.get(id=gare_arr_id)

            # Calcul du tarif par zones
            nb_segments = abs(g_arr.commune.position - g_dep.commune.position)
            tarifs = {0: 200, 1: 200, 2: 300, 3: 400, 4: 500, 5: 600}
            prix_final = tarifs.get(nb_segments, 800)

            sens_voyage = 'ALLER' if g_dep.commune.position < g_arr.commune.position else 'RETOUR'

            voyages = Voyage.objects.filter(
                sens=sens_voyage,
                jour_depart=date.today(),
                heure_depart__gte=limite_visibilite,
                est_ouvert=True
            ).order_by('heure_depart')

            for v in voyages:
                v.prix_a_payer = prix_final
                v.dep_user = g_dep.nom
                v.arr_user = g_arr.nom

                # INJECTION DE L'HEURE APPROXIMATIVE[cite: 4, 5]
                decalage = v.get_heure_passage(g_dep)
                v.heure_affichage = (datetime.combine(date.today(), v.heure_depart) + decalage).time()

                v.statut = "EN COURS" if v.heure_affichage <= heure_actuelle else "À VENIR"
                v.peut_reserver = v.heure_affichage > heure_actuelle

            return render(request, 'transport/resultats.html', {
                'voyages': voyages,
                'gares': gares,
                'depart': g_dep,
                'arrivee': g_arr,
                'prix_total': prix_final
            })

        except (Gare.DoesNotExist, ValueError):
            pass

    # 2. AFFICHAGE PAR DÉFAUT (HOME - Heure brute Admin)[cite: 5]
    voyages_defaut = Voyage.objects.filter(
        jour_depart=date.today(),
        heure_depart__gte=limite_visibilite,
        est_ouvert=True
    ).order_by('heure_depart')

    for v in voyages_defaut:
        v.heure_affichage = v.heure_depart  # Heure brute pour la home[cite: 5]
        v.statut = "EN COURS" if v.heure_depart <= heure_actuelle else "À VENIR"
        v.peut_reserver = v.heure_depart > heure_actuelle
        v.dep_user = v.gare_depart_defaut.nom if v.gare_depart_defaut else "Anyama"
        v.arr_user = v.gare_arrivee_defaut.nom if v.gare_arrivee_defaut else "Port-Bouët"
        v.prix_a_payer = 500

    return render(request, 'transport/home.html', {
        'voyages': voyages_defaut,
        'gares': gares,
        'prix_total': 0
    })


def reserver_etape_1(request, voyage_id):
    voyage = get_object_or_404(Voyage, id=voyage_id)
    return render(request, 'transport/form_passager.html', {
        'voyage': voyage,
        'gare_dep': request.GET.get('dep'),
        'gare_arr': request.GET.get('arr'),
        'prix': request.GET.get('prix')
    })


def valider_reservation(request, voyage_id):
    """Validation et création de ticket avec heure réelle enregistrée"""
    if request.method == 'POST':
        voyage = get_object_or_404(Voyage, id=voyage_id)

        # Récupération de la gare de départ pour figer l'heure sur le ticket[cite: 6]
        nom_gare_dep = request.POST.get('gare_dep')
        gare_obj = Gare.objects.filter(nom=nom_gare_dep).first()

        # Calcul de l'heure exacte de passage pour ce passager[cite: 4, 6]
        decalage = voyage.get_heure_passage(gare_obj) if gare_obj else timedelta(0)
        heure_ticket = (datetime.combine(date.today(), voyage.heure_depart) + decalage).time()

        code = f"KNEKT-{str(uuid.uuid4())[:4].upper()}"

        res = Reservation(
            voyage=voyage,
            nom_passager=request.POST.get('nom'),
            prenom_passager=request.POST.get('prenom'),
            gare_depart_nom=nom_gare_dep,
            gare_arrivee_nom=request.POST.get('gare_arr'),
            prix_paye=int(request.POST.get('prix', 0)),
            mode_paiement=request.POST.get('payment_mode'),
            code_ticket=code,
            paye=True
        )

        # On stocke l'heure calculée pour le rendu du ticket[cite: 6]
        res.heure_reelle_ticket = heure_ticket

        # Génération du QR Code
        qr_url = f"http://127.0.0.1:8000/scan/{code}/"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#FF8200", back_color="white")

        blob = BytesIO()
        img.save(blob, 'PNG')

        # Sauvegarde du QR code dans le champ image de la réservation
        if hasattr(res, 'qr_code'):
            res.qr_code.save(f'{code}.png', File(blob), save=False)

        res.save()
        return render(request, 'transport/ticket.html', {'res': res})
    return redirect('home')


@login_required(login_url='login')
def mes_tickets(request):
    # On filtre par le nom de l'utilisateur connecté pour simplifier
    tickets = Reservation.objects.filter(
        nom_passager__iexact=request.user.last_name
    ).order_by('-date_reservation')
    return render(request, 'transport/mes_tickets.html', {'tickets': tickets})


def voir_ticket(request, code_ticket):
    res = get_object_or_404(Reservation, code_ticket=code_ticket)
    return render(request, 'transport/ticket.html', {'res': res})


# --- VUES AGENTS ---

@staff_member_required
def dashboard_agent(request):
    total_tickets = Reservation.objects.count()
    revenu_total = Reservation.objects.aggregate(Sum('prix_paye'))['prix_paye__sum'] or 0
    query = request.GET.get('q', '').strip()
    resultat = Reservation.objects.filter(code_ticket__iexact=query).first() if query else None

    return render(request, 'transport/agent_dashboard.html', {
        'total_tickets': total_tickets,
        'revenu_total': revenu_total,
        'resultat': resultat,
        'query': query,
        'derniers_tickets': Reservation.objects.all().order_by('-date_reservation')[:10]
    })


def valider_ticket_scan(request, code_ticket):
    ticket = get_object_or_404(Reservation, code_ticket=code_ticket)
    if ticket.est_valide:
        ticket.est_valide = False
        ticket.date_utilisation = timezone.now()
        ticket.save()
        message, couleur = "✅ TICKET VALIDE", "green"
    else:
        message, couleur = "❌ DÉJÀ UTILISÉ", "red"
    return render(request, 'transport/scan_result.html', {'ticket': ticket, 'message': message, 'couleur': couleur})


# --- AUTH ---

def inscription_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'transport/inscription.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'transport/login.html', {'error': "Identifiants invalides"})


def logout_view(request):
    logout(request)
    return redirect('home')