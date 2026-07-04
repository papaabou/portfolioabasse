# Guide rapide — ajouter tes photos et vidéos

## 1. Lancer le site en local

```
cd portfolio
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Ouvre ensuite http://127.0.0.1:8000/

## 2. Se connecter à l'admin

Va sur http://127.0.0.1:8000/admin/

Identifiant : `abasse`
Mot de passe : `Portfolio2026!`

(Pense à changer ce mot de passe une fois connecté : Admin → Utilisateurs → abasse → "Changer le mot de passe")

## 3. Où mettre tes photos et vidéos (depuis ta clé USB)

### Pour chaque projet (section "Projects" > "Projects")
Clique sur un projet existant (ou "Ajouter Project"), puis dans le bloc **"Images et video"** :

- **Thumbnail** : l'image principale affichée dans la liste des réalisations et sur la page d'accueil
- **Image** : image de secours si pas de thumbnail
- **Video file** : pour uploader directement un fichier vidéo depuis ta clé
- **Video url** : si ta vidéo est déjà sur YouTube ou Vimeo, colle juste le lien ici (le lecteur s'affiche automatiquement sur la page du projet)
- **Live url** : lien externe (site du client, post Instagram, etc.)

Plus bas sur la page, tu as une section **"Project images"** : c'est la galerie. Tu peux ajouter autant de photos que tu veux pour ce projet, avec une légende pour chacune.

### Pour ta photo de profil
"About me" > "Profiles" > clique sur ton profil > champ **profile_image**

### Pour le logo et favicon du site
"Core" > "Site Settings" > champs **logo** et **favicon**

### Pour tes liens (réseaux sociaux, etc.)
"About me" > "Social links" > "Ajouter Social link"
Donne un nom (ex: "LinkedIn", "YouTube", "TikTok") et colle l'URL.
Ces liens apparaissent automatiquement dans le header, le footer et la page contact — pas besoin de modifier le code.

## 4. Ce que j'ai déjà corrigé

- Les sections "Services", "À propos" et les liens de contact sur la page d'accueil étaient codés en dur (toujours les mêmes, peu importe l'admin) — ils utilisent maintenant les vraies données de la base.
- Les liens Behance/Instagram étaient répétés en dur dans plusieurs pages — ils viennent maintenant tous de "Social links", donc un seul endroit à mettre à jour.
- Le formulaire de contact ne plantera plus en local s'il n'y a pas de configuration email (les emails s'affichent juste dans le terminal en mode développement).
- Création d'un compte admin utilisable : `abasse` / `Portfolio2026!`

## 5. Ce qu'il reste à faire de ton côté

- Uploader tes vraies photos/vidéos pour les 10 projets déjà créés (ils sont vides pour l'instant)
- Remplir ton email et ton numéro WhatsApp dans "About me" > "Profiles" pour que les boutons de contact fonctionnent
- Me dire si tu veux qu'on ajoute d'autres projets, ou qu'on travaille le design plus en détail
