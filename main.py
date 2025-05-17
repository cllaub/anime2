# import

from flask import Flask, render_template, redirect, session, request
import pymongo

# on créé l'app

app = Flask("Projet2")
app.secret_key = "l'électricien"

mongo = pymongo.MongoClient("mongodb+srv://clemlaubgeek360:magicmaker@cluster0.7auv6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
BDD_utilisateur = mongo.BDD.utilisateurs
mon_utilisateur = BDD_utilisateur.find_one({"pseudo":"clem"})
print(mon_utilisateur)


@app.route('/')
def acceuil() :
    mes_annonces = mongo.BDD.annonces
    annonces = mes_annonces.find({})
    if "utilisateur" in session:
        mes_utilisateurs = mongo.BDD.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session['utilisateur']})
        print(utilisateur)
        return render_template("index.html", utilisateur = utilisateur,
                               annonces = annonces)
    else:
         return render_template("index.html", annonces = annonces)

@app.route('/profil')
def profil() :
    mes_utilisateurs = mongo.BDD.utilisateurs
    utilisateur = mes_utilisateurs.find_one({"pseudo" : session['utilisateur']})
    print(utilisateur)
    return render_template("profil.html", utilisateur = utilisateur)

@app.route('/logout')
def logout() :
    session.clear()
    return redirect('/')

@app.route('/login', methods= ["GET", "POST"])
def login() :
    if request.method == "GET":
        return render_template("login.html")
    else:
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        mes_utilisateurs = mongo.BDD.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        if not utilisateur :
            return render_template("login.html" , erreur = "l'utilisateur n'existe pas")
        elif mdp_entre != utilisateur["mdp"] :
            return render_template("login.html" , erreur = "le mot de passe est incorrect")
        else :
            session['utilisateur'] = pseudo_entre
            return redirect('/')

@app.route('/register', methods= ["GET", "POST"])
def register() :
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 1 : on récupère les informations entrées dans les inputs
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        avatar_entre = request.form["input_avatar"]
        if avatar_entre == "" :
            avatar_entre = "data:image/jpeg;base64,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"        
        # 2 : on gère tous les cas d'erreurs
        mes_utilisateurs = mongo.BDD.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        if utilisateur:
            return render_template("register.html" , erreur = "l'utilisateur existe déjà")
        elif pseudo_entre == "" :
            return render_template("register.html", erreur = "veuillez rentrer un pseudo")
        elif len(mdp_entre) < 4 :
            return render_template("register.html", erreur = "le mot de passe doit faire au moins 4 caractère")
        else :
        
        # 3 : on crée le compte utilisateur
            mes_utilisateurs.insert_one({
                "pseudo" : pseudo_entre,
                "mdp" : mdp_entre,
                "avatar" : avatar_entre,
                "age" : 0,
                "nationnalité" : "non précisée"
            })
            session["utilisateur"] = pseudo_entre
            return redirect('/')

@app.route('/recherche')
def recherche() :
        return render_template("recherche.html")
#route admin
@app.route("/admin/anime")
def anime():
    db_post = mongo.BDD.annonces
    mes_post = db_post.find({})
    return render_template("admin/anime.html",
                           mes_post = list(mes_post))



@app.route('/supprimer_post/<titre>')
def supprimer_post(titre) :
        db_post = mongo.BDD.annonces
        db_post.delete_one({"titre" : titre})
        return redirect("/admin/anime")


# on lance l'app
app.run("0.0.0.0", "3904")
