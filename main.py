import os, sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import webbrowser, sqlite3, os, random, threading, time
from datetime import datetime
from SUBSCRIPTS.MyHash import DoubleHashing
from SUBSCRIPTS.classes import Parents, Enfants, HistoFiles


"""
Ce fichier est le fichier principal du projet.
Il est constitué de 20 fonctions dont 17 sont liés à l'arborescence de l'application flask.
Le fichier commence par vérifier la présence de tous les fichiers nécessaires au fonctionnement de l'application.
Il va ensuite initialiser les bases de données dans le fichier de sauvegarde si aucun fichier n'a été trouvé.
Un thread sera ensuite lancé pour reprendre la vérification des virements de l'argent de poche des enfants.
Enfin, l'application flask sera lancée après avoir ouvert le navigateur par défaut à l'adresse de la page.
"""




# Initialisation et vérification de tous les fichiers

fichiers_db = ["database.db"]
fichiers_py = ["MyHash.py", "classes.py"]
fichiers_HTML = ["connexion.html", "creation.html", "dashboard.html", "editer.html", "historique.html",
                 "inscription.html", "message.html", "profils.html"]
fichiers_CSS = ["style.css", "styles.css", "dashboard.css", "edit.css", "histo.css"]
fichiers_JS = ["script.js"]


def DB_check(file):
    """
    Cette fonction va vérifier que le fichier de souvegarde donné en argument existe.
    Si ce dernier n'existe pas, alors il est créé.
    :param file:
    :return: booléen
    """
    if not os.path.exists(file):
        try:
            with open(file, 'w', newline='') as f:
                pass
            print(f"|Le fichier de sauvegarde a été créé")

        except Exception as e:
            print(f"|Erreur lors de la création du fichier de sauvegarde: {e}")
            return False
    else:
        print(f"|Le fichier de sauvegarde a bien été trouvé")
    return True

def must_have_check(file):
    """
    Cette fonction va vérifier l'existance d'un fichier donné.
    :param file:
    :return: booléen
    """
    if not os.path.exists(file):
        print(f"Erreur : {file} manquant")
        return False
    else:
        return True

print("|=========================================")
for file in fichiers_db:
    DB_check(f"{file}")
c = 0
for file in fichiers_py:
    if must_have_check(f"SUBSCRIPTS/{file}"):
        c += 1
print(f"|{c}/{len(fichiers_py)} fichier(s) PY trouvé(s).")
c = 0
for file in fichiers_HTML:
    if must_have_check(f"templates/{file}"):
        c += 1
print(f"|{c}/{len(fichiers_HTML)} fichier(s) HTML trouvé(s).")
c = 0
for file in fichiers_CSS:
    if must_have_check(f"static/css/{file}"):
        c += 1
print(f"|{c}/{len(fichiers_CSS)} fichier(s) CSS trouvé(s).")
c = 0
for file in fichiers_JS:
    if must_have_check(f"static/js/{file}"):
        c += 1
print(f"|{c}/{len(fichiers_JS)} fichier(s) JS trouvé(s).")
print("|=========================================")

# Création des tables SQL
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS utilisateurs (
    nom_utilisateur TEXT NOT NULL PRIMARY KEY,
    mot_de_passe TEXT NOT NULL
)''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS enfants (
    global_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_parent INTEGER NOT NULL,
    nom TEXT NOT NULL,
    genre TEXT NOT NULL,
    montant_depart INTEGER NOT NULL,
    porte_monnaie INTEGER NOT NULL,
    montant_dajout INTEGER,
    frequence INTEGER,
    horloge TEXT,
    compte_bancaire TEXT,
    compte_paypal TEXT,
    avatar TEXT
)
''')
conn.commit()
conn.close()

# ====================================
# ====================================
# ====================================
# ====================================
# ====================================
# ====================================



# FONCTIONS FLASK

app = Flask(__name__, template_folder='./templates/')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET', 'POST'])
def connexion():
    """
    Cette fonction va permettre de renvoyer vers la page de connexion à la racine de l'application flask.
    :return: connexion.html
    """
    return render_template("connexion.html")


@app.route('/inscription')
def inscription():
    """
    Cette fonction va permettre de renvoyer vers la page d'inscription à /inscription dans l'arborescence de l'application flask.
    :return: inscription.html
    """
    return render_template('inscription.html')


@app.route('/profils')
def profils():
    """
    Cette fonction controle l'accès à la page profils.html.
    Des informations concernants les enfant de l'utilisateur seront renvoyé vers cette page.
    :return: profils.html ou connexion.html
    """
    if 'nom_utilisateur' in session:
        id_parent = session['nom_utilisateur']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enfants WHERE id_parent = ?", (id_parent,))
        enfants_raw = cursor.fetchall()
        enfants = []

        for enfant in enfants_raw:
            enfants.append(enfant)

        enfants_count = len(enfants)
        conn.close()
        return render_template('profils.html', enfants=enfants, enfants_count=enfants_count)
    else:
        return redirect('/')


@app.route("/creation_page", methods=['GET', 'POST'])
def creation_page():
    """
    Cette fonction controle l'accès à la page creation.html.
    :return: creation.html ou connexion.html
    """
    if 'nom_utilisateur' in session:
        return render_template("creation.html")
    else:
        return redirect('/')


# Formulaire de connexion
@app.route('/connexion', methods=['POST'])
def verifier_connexion():
    """
    Cette fonction va comparer les données du formulaire reçues depuis connexion.html pour les comparer avec la database.
    Selon la validité des informations données, l'utilisateur pourra accéder ou non à la page de profils.
    :return: profils.html ou message.html
    """
    nom_utilisateur = request.form['nom']
    mot_de_passe = request.form['mdp']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nom_utilisateur, mot_de_passe FROM utilisateurs WHERE nom_utilisateur = ?',
                   (nom_utilisateur,))
    utilisateur = cursor.fetchone()  # Récupère une ligne correspondante

    if utilisateur:
        # Utilisateur trouvé, vérification du mot de passe
        if utilisateur[1] == DoubleHashing.double_hash(mot_de_passe):
            session['nom_utilisateur'] = nom_utilisateur  # Stocke le nom de l'utilisateur dans la session
            conn.close()
            return redirect(url_for('profils'))  # Rediriger vers la route 'profils'
        else:
            conn.close()
            session['message'] = f"Connexion impossible, nom d'utilisateur ou mot de passe incorrect."
            session['redirect_link'] = "/"
            return redirect(url_for('message'))
    else:
        session['message'] = f"Connexion impossible, nom d'utilisateur ou mot de passe incorrect."
        session['redirect_link'] = "/"
        return redirect(url_for('message'))


# Formulaire d'inscription
@app.route("/inscription", methods=["GET", "POST"])
def soumettre():
    """
    Cette fonction va récupérer les données du formulaire de la page inscription.html.
    Selon les données reçues, l'utilisateur sera créé ou non.
    :return: message.html
    """
    user = request.form['nom']
    mdp = request.form['mdp']
    obj = Parents(user, DoubleHashing.double_hash(mdp))

    # Connexion et tentative d'ajout dans la DB
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (?, ?)",
                       (obj.username, obj.passwd))
        conn.commit()
        session['message'] = "Compte créé avec succès!"
        session['redirect_link'] = "/"
    except sqlite3.IntegrityError:
        session['message'] = "Impossible de créer ce compte, nom d'utilisateur déjà pris."
        session['redirect_link'] = "/inscription"

    # Fermeture DB et redirection
    conn.close()
    return redirect(url_for('message'))


@app.route('/message')
def message():
    """
    Cette fonction va stocker les éléments de session['message'] et de session["redirect_link"].
    Par la même occasion elle va supprimer ces éléments de la session pour ensuite donner les variables à la page message.html
    :return: message.html ; args : message, redirect_link
    """
    message = session.pop('message', 'Une erreur est survenue, veuillez réessayer.')
    redirect_link = session.pop('redirect_link', '/')
    return render_template('message.html', message=message, redirect_link=redirect_link)


@app.route('/creation', methods=['POST'])
def creation():
    """
    Cette fonction va permettre la création d'un profil enfant tout en controlant l'accès de la page.
    Les données du formulaire de la page creation.html vont être récupérées puis ajoutées à la table enfants si les conditions sont favorables.
    De plus la photo de profil sera désigné aléatoirement selon le genre de l'enfant.
    :return: message.html
    """
    if 'nom_utilisateur' in session:
        prenom = request.form.get('prenom')
        montant_d = request.form.get('montant_d')
        montant_p = request.form.get('montant_p')
        rib = request.form.get('rib')
        paypal = request.form.get('paypal')
        genre = request.form.get('genre')
        frequence = request.form.get('frequence')
        horloge = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        obj = Enfants(session['nom_utilisateur'], prenom, genre, montant_d, montant_d, montant_p, frequence, horloge,
                      rib, paypal)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM enfants WHERE id_parent = ? AND nom = ?", (session['nom_utilisateur'], prenom))
        existing_child = cursor.fetchone()

        if existing_child:
            session['message'] = f"Le nom {prenom} existe déjà pour un enfant de votre famille."
            session['redirect_link'] = "/creation_page"
        else:
            # Determine avatar image based on genre
            if genre == 'garcon':
                image = random.choice(["Garcon3.png", "Garcon4.png", "Garcon5.png", "Garcon6.png", "Garcon7.png", "Garcon8.png"])
            else:
                image = random.choice(["Fille3.png", "Fille4.png", "Fille5.png", "Fille6.png", "Fille7.png", "Fille8.png"])

            try:
                cursor.execute(
                    "INSERT INTO enfants (id_parent, nom, genre, montant_depart, porte_monnaie, montant_dajout, frequence, horloge, compte_bancaire, compte_paypal, avatar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (obj.id_parent, obj.nom, obj.genre, obj.montant_depart, obj.porte_monnaie,
                     obj.montant_dajout, obj.frequence, obj.horloge, obj.compte_bancaire, obj.compte_paypal, image))
                conn.commit()
                session['message'] = f"Profil de {obj.nom} créé avec succès!"
                session['redirect_link'] = "/profils"

            except sqlite3.IntegrityError:
                session['message'] = "Oops, une erreur est survenue. Veuillez réessayer :/"
                session['redirect_link'] = "/creation_page"

        # Fermeture DB et redirection
        conn.close()
        return redirect(url_for('message'))

    else:
        return redirect('/')


@app.route('/select_enfant/<string:nom_enfant>', methods=['GET'])
def select_enfant(nom_enfant):
    """
    Cette fonction est utilisée par la page profils.html.
    Elle permet de faire le lien entre l'enfant sur lequel l'utilisateur a cliqué et le code si besoin.
    :param nom_enfant: nom de l'enfant sur lequel l'utilisateur a cliqué dans profils.html
    :return: dashboard.html
    """
    if 'nom_utilisateur' in session:
        session['enfant'] = nom_enfant
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Cette fonction va controler l'accès à la page dashboard.html.
    De plus elle va collecter les données de l'enfant qui seront par la suite affichées sur dashboard.html.
    :return: dashboard.html ou profils.html ou connexion.html
    """
    if 'enfant' in session:
        nom_enfant = session['enfant']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM enfants WHERE nom = ? AND id_parent = ?",
            (nom_enfant, session["nom_utilisateur"]))
        enfant_data = cursor.fetchone()
        conn.close()


        if enfant_data:
            solde, compte_paypal, compte_bancaire, avatar = enfant_data[5], enfant_data[10], enfant_data[9], enfant_data[
                11]
            return render_template('dashboard.html', enfant=enfant_data, nom_enfant=nom_enfant, solde=solde,
                                   compte_paypal=compte_paypal,
                                   compte_bancaire=compte_bancaire, avatar=avatar)
        else:
            return redirect(url_for('profils'))
    else:
        return redirect(url_for('connexion'))


@app.route('/ajouter_argent/<string:nom_enfant>/<int:montant>', methods=['GET'])
def ajouter_argent(nom_enfant, montant, op=0, parent=None):
    """
    Cette fonction est utilisé de deux façons différente :
        -Un ajout classique via le dashboard de l'enfant
        -Les ajout d'argent de poche
    Dans le premier cas, les deux derniers arguments se seront pas données puisqu'il s'agit de l'opération par défaut.
    Dans le second cas, l'opérateur va changer afin d'ajouter les bonnes valeurs à l'historique des transactions.
    Cette fonction va donc permettre de créditer le compte d'un enfant et d'ajouter cette transaction à son historique.
    :param nom_enfant: nom de l'enfant
    :param montant: somme qui va être créditée au compte
    :param op: 0:ajout dashboard ; 1:ajout d'argent de poche
    :param parent: parent/nom d'utilisateur de l'enfant
    :return: message sur le dashboard ou None
    """
    if parent is None:
        parent = session["nom_utilisateur"]
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE enfants SET porte_monnaie = porte_monnaie + ? WHERE nom = ? AND id_parent = ?",
                   (montant, nom_enfant, parent))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT global_id FROM enfants WHERE nom = ? AND id_parent = ?",
                   (nom_enfant, parent))
    gid = cursor.fetchone()[0]
    if op == 0:
        HistoFiles(gid).push_files("AJOUT", "AJOUT", str(montant) + "€")
    elif op == 1:
        HistoFiles(gid).push_files("AJOUT", "VIREMENT EN VOTRE FAVEUR", str(montant) + "€")
    conn.commit()
    conn.close()
    with app.app_context():
        return jsonify({'success': True, 'message': f"{montant}€ ajouté avec succès à {nom_enfant}."})


@app.route('/retirer_argent/<string:nom_enfant>/<int:montant>/<string:select>', methods=['GET'])
def retirer_argent(nom_enfant, montant, select):
    """
    Cette fonction est utilisée pour soustraire une somme au solde d'un enfant.
    Elle est utilisée par la page dashboard.html.
    Une fois la table de l'enfant mise à jour, la fonction ajoute la transaction à l'historique avec le moyen de retrait employé.
    :param nom_enfant: nom de l'enfant
    :param montant: somme soustraite au solde de l'enfant
    :param select: CASH/PAYPAL/BANQUE:type de retrait utilisé
    :return: message sur le dashboard
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT porte_monnaie FROM enfants WHERE nom = ? AND id_parent = ?",
                   (nom_enfant, session["nom_utilisateur"]))
    porte_monnaie_actuel = cursor.fetchone()[0]
    if porte_monnaie_actuel >= montant:
        cursor.execute("UPDATE enfants SET porte_monnaie = porte_monnaie - ? WHERE nom = ? AND id_parent = ?",
                       (montant, nom_enfant, session["nom_utilisateur"]))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT global_id FROM enfants WHERE nom = ? AND id_parent = ?",
                       (session["enfant"], session["nom_utilisateur"]))
        gid = cursor.fetchone()[0]
        HistoFiles(gid).push_files(select, "RETRAIT", str(montant)+"€")
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f"{montant}€ retiré avec succès de {nom_enfant}."})
    else:
        conn.close()
        return jsonify({'success': False,
                        'message': f"Impossible de retirer {montant}€ de {nom_enfant} car le solde est insuffisant."})


@app.route('/dashboard/<string:nom_enfant>', methods=['GET'])
def get_solde(nom_enfant):
    """
    Cette fonction va permettre de récupérer le solde d'un enfant pour pouvoir mettre à jour ce dernier après une opération.
    :param nom_enfant: nom de l'enfant
    :return: solde de l'enfant
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT porte_monnaie FROM enfants WHERE nom = ? AND id_parent = ?",
                   (nom_enfant, session["nom_utilisateur"]))
    solde = cursor.fetchone()[0]
    conn.close()
    return jsonify({'success': True, 'solde': solde})


@app.route('/editer')
def editer():
    """
    Cette fonction va permettre de récupérer toutes les données de l'enfant présent dans la session.
    Ces données sont ensuite renvoyées à la page editer.html qui pourra afficher les informations de l'enfant.
    :return: editer.html
    """
    if 'enfant' in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enfants WHERE nom = ? AND id_parent = ?",
                       (session["enfant"], session["nom_utilisateur"]))
        enfant = cursor.fetchall()
        conn.close()
        return render_template('editer.html', enfant=enfant)
    else:
        return redirect('/profils')


@app.route('/modification', methods=['POST'])
def modification():
    """
    Cette fonction va permettre de modifier les informations d'un enfant via la page editer.html.
    Les données du formulaire de la page sont récupérées puis vérifiées.
    Si les conditions sont respectées, alors les informations de l'enfant sont mises à jour.
    :return: message.html ou profils.html
    """
    if 'enfant' in session:
        # Récupération des données du formulaire
        prenom = request.form.get('prenom')
        montant_p = request.form.get('montant_p')
        rib = request.form.get('rib')
        paypal = request.form.get('paypal')
        genre = request.form.get('genre')
        frequence = request.form.get('frequence')

        # Choix de l'avatar en fonction du genre
        new_avatar = random.choice(["Garcon3.png", "Garcon4.png", "Garcon5.png", "Garcon6.png", "Garcon7.png", "Garcon8.png"]) if genre == 'garcon' else random.choice(["Fille3.png", "Fille4.png", "Fille5.png", "Fille6.png", "Fille7.png", "Fille8.png"])

        # Connexion à la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Vérification de l'existence d'un autre enfant avec le même nom
        cursor.execute("SELECT * FROM enfants WHERE id_parent = ? AND nom = ? AND nom != ?",
                       (session['nom_utilisateur'], prenom, session['enfant']))
        existing_child = cursor.fetchone()

        if not existing_child or session['enfant'] == prenom:
            # Mise à jour du profil de l'enfant
            cursor.execute("""
                           UPDATE enfants
                           SET nom=?, montant_dajout=?, compte_bancaire=?, compte_paypal=?, genre=?, frequence=?, avatar=?
                           WHERE nom=? AND id_parent=?
                       """, (prenom, montant_p, rib, paypal, genre, frequence, new_avatar, session['enfant'], session["nom_utilisateur"]))
            session['enfant'] = prenom  # Mise à jour de la session avec le nouveau nom si changé
            session['message'] = f"Profil de {prenom} modifié avec succès!"
            session['redirect_link'] = "/dashboard"
        else:
            # Gérer le cas où un autre enfant avec le même nom existe déjà
            session['message'] = f"Le nom {prenom} existe déjà pour un enfant de votre famille. Impossible de modifier le profil."
            session['redirect_link'] = "/dashboard"

        # Fermeture de la connexion à la base de données
        conn.commit()
        conn.close()
        return redirect(url_for('message'))
    else:
        return redirect('/profils')




@app.route('/historique')
def historique():
    """
    Cette fonction va permettre de consulter l'historique de l'enfant.
    Elle va aller chercher le global_id de l'enfant souhaité pour ensuite stocker les données de l'historique.
    Ces données seront envoyées à la page historique.html qui les traduira en un affichage correct.
    :return: historique.html ou profils.html
    """
    if 'enfant' in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT global_id FROM enfants WHERE nom = ? AND id_parent = ?",
                       (session["enfant"], session["nom_utilisateur"]))
        gid = cursor.fetchone()[0]
        transactions = HistoFiles(gid).get_files()
        transactions.reverse()
        conn.commit()
        conn.close()
        return render_template('historique.html', transactions=transactions)
    else:
        return redirect('/profils')


@app.route('/logout')
def logout():
    """
    Cette fonction permet de supprimer tous les éléments de la session et de rediriger vers la page de connexion.
    :return: connexion.html
    """
    if 'nom_utilisateur' in session:
        session.clear()
    return redirect('/')


def schedule_money_addition():
    """
    Cette fonction va permettre de vérifier continuellement si il faut faire le virement automatique aux enfants.
    Elle tourne à l'aide de thread donc indépendamment du reste.
    Toutes les 60 secondes, la fonction va récupérer tous les enfants de la table enfants.
    Si le jour, l'heure et la minute correspondent, alors le viremment sera effectué pour les enfants concernés.
    :return:
    """
    print("Pendule d'ajout d'argent en cours d'execution...")
    while True:
        now = datetime.now()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enfants")
        enfants = cursor.fetchall()
        conn.commit()
        conn.close()
        for enfant in enfants:
            if enfant[7] == "hebdomadaire" and now.weekday() == 0 and now.hour == 0 and now.minute == 0:
                with app.app_context():
                    ajouter_argent(enfant[2], enfant[6], 1, enfant[1])
            if enfant[7] == "mensuelle" and now.day == 1 and now.hour == 0 and now.minute == 0:
                with app.app_context():
                    ajouter_argent(enfant[2], enfant[6], 1, enfant[1])
        time.sleep(60)

# RUN
thread = threading.Thread(target=schedule_money_addition)
thread.start()
