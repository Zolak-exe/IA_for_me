Bonjour,

Voici la réponse à votre projet d'importation de véhicules en Python :

1. Fichiers à créer :
* Frontend (Web) : /frontend
* API Gateway : /api-gateway
* Backend (API) : /backend
* Database : /database
* Authentication & Authorization : /authentication-authorization
* Third-Party Services : /third-party-services
* Storage : /storage
2. Code complet :
* Frontend (Web) :
	+ index.html
	+ style.css
	+ script.js
* API Gateway :
	+ api_gateway.py
* Backend (API) :
	+ backend.py
* Database :
	+ database.py
* Authentication & Authorization :
	+ authentication-authorization.py
* Third-Party Services :
	+ stripe.py
	+ paypal.py
	+ email_service_provider.py
	+ sms_gateway.py
	+ google_maps_api.py
* Storage :
	+ amazon_s3.py
	+ google_cloud_storage.py
3. Dépendances :
* Frontend (Web) :
	+ HTML/CSS/JS
	+ React (ou Vue)
* API Gateway :
	+ Spring Cloud Gateway
	+ Kong
* Backend (API) :
	+ Node.js avec Express ou Python Flask
* Database :
	+ MySQL ou PostgreSQL
* Authentication & Authorization :
	+ JWT
	+ OAuth
* Third-Party Services :
	+ Stripe
	+ PayPal
	+ Email Service Provider
	+ SMS Gateway
	+ Google Maps API
* Storage :
	+ Amazon S3
	+ Google Cloud Storage
4. Modules principaux et leur responsabilités :
	+ Frontend (Web) : fournit l'interface utilisateur pour les clients.
	+ API Gateway : fournit une entrée unique pour les requêtes HTTP à toutes les APIs de backend.
	+ Backend (API) : fournit des services pour gérer le contenu, les devis, les commandes, et les données clients.
	+ Authentication & Authorization : fournit des mécanismes d'authentification et d'autorisation pour protéger les informations sensibles.
	+ Third-Party Services : fournit des services tiers de paiement, messagerie, SMS, mappage, etc.
	+ Storage : fournit des services de stockage de données tels que l'enregistrement de devis personnalisés et d'images des véhicules.
5. Interfaces publiques entre les modules : Les interfaces entre les modules sont définies dans le diagramme composants ci-dessus.
6. Requirements :
	+ Contexte et Objectifs : l'entreprise souhaite créer un site web professionnel pour une entreprise spécialisée dans l'importation de véhicules (voitures, motos, utilitaires, etc.) depuis tout le secteur de l'Europe vers la France. Objectifs principaux : vente en ligne d'une prestation d'import de véhicules (neufs/occasion), vitrine d'exemples de véhicule importée avec les comparaisons financières, information sur les procédures d'importation (étapes, douanes, homologation, taxes), devis personnalisés pour les clients, FAQ sur les réglementations et conseils.
	+ Fonctionnalités techniques obligatoires :
		- Frontend (Interface Utilisateur) : design responsive (mobile/desktop/tablette) avec un style moderne/minimaliste/luxe/racing. Page d'accueil avec bannière hero (nom de l'entreprise avec le slogan suivant : Votre partenaire de confiance pour l'importation de véhicules depuis toute l'Europe). Vitrines d'exemples (Slideshow vitrines de véhicule avec photo nom et prix import versus prix français : type bmw m3 f80, nissan 350z, ford focus rs). Devis de recherche avancés (marque, modèle, année, prix, kilométrage option et critères supplémentaires et informations de celui qui veut un devis). Témoignages clients et partenariats (ex: clients, transporteurs, garages).
		- Backend (Administration) : tableau de bord pour gérer : base de données des devis envoyés, ajout/modification/suppression de véhicules de la vitrine (avec upload d'images/vidéos), suivi des commandes et envoi de notifications automatiques (ex: 'Votre véhicule est arrivé au port'). Base de données clients (CRM basique). Intégrations : paiement en ligne (Stripe, PayPal, virement bancaire). Module de devis automatique (calcul des coûts : achat + transport + douanes + homologation). Chatbox (pour répondre aux questions fréquentes sur les délais ou documents et échanger avec les clients). Sécurité : certificat SSL (HTTPS). Protection contre les fraudes (vérification des documents clients). Sauvegardes automatiques des données. Base de Données : modèle de données pour : devis (ID Clients, toute les information compléter dans le formulaire de devis en frontend) véhicules (ID, marque, modèle, année, VIN, prix, statut, photos, etc.). Clients (ID, nom, email, adresse, historique). Commandes (ID, véhicule, client, statut, date, documents joints). Partenaires (transporteurs, garages agrées).
	+ Design et Expérience Utilisateur (UX/UI) : style visuel : professionnel/luxe/sportif/épuré avec une palette de couleurs dominantes (ex: rouge nuancé + or pour le luxe, noir). Logo : à créer ou à intégrer (fournir le fichier si existant). Polices : orbitron sans serif pour les titres, Open Sans pour le texte. Éléments clés : boutons d'appel à l'action (CTA) visibles (ex: 'Demander un devis', 'Voir le véhicule'). Icônes intuitives pour les étapes d'importation (ex: 🚢→📄→💰→🚗). Galerie photo/vidéo haute résolution pour chaque véhicule. Animation légère au scroll (ex: effets de fondu pour les sections). Exemples de sites inspirants : Comme koumaz.infinityfreeapp.com/?i=2, pour la structure et la colorimétrie. Comme stripe.com/fr, pour la fluidité et les animations. Comme www.apple.com/fr, pour le professionnalisme.
	+ Contenu et SEO : contenu à inclure : textes : pages légales obligatoires : CGV, politique de confidentialité, mentions légales (adaptées au pays). Mots-clés SEO à cibler : 'Import voiture [pays] pas cher', 'Acheter une voiture japonaise, allemande en france', 'Homologation véhicule importé [pays]', etc. Optimisation technique SEO : balises meta, URLs propres, vitesse de chargement < 2s. Schema markup pour les véhicules (rich snippets dans Google). Sitemap XML et fichier robots.txt. Multilingue : oui Si oui, langues à inclure (ex: français, anglais, suisse, allemands, belge, espagnole, italien).
	+ Hébergement et Performance : recommandations pour l'hébergement : type : hébergement gratuit (Oracle Cloud Free Tier).
	+ Légal et Conformité : points légaux à intégrer : réglementations : affichage obligatoire des prix TTC (taxes douanières incluses si possible). Informations sur les droits de douane et TVA pour [pays de destination]. Certificats requis (ex: certificat de conformité EU, quitus fiscal). Protection des données : RGPD si ciblant l'Europe (formulaire de consentement cookies, droit à l'oubli). Sécurisation des données clients (chiffrement). Conditions générales : délais de livraison (ex: 4-8 semaines selon le pays). Politique de retour/annulation (ex: 'Délai de rétractation de 14 jours').
	+ Livrables et Délais : attentes pour le projet : livrables : code source commenté (frontend: HTML/CSS/JS + framework [React/Vue]), backend: [Node.js/Python/PHP]). Base de données prête à l'emploi (MySQL/PostgreSQL). Documentation technique pour la maintenance.
7. Exemples de prompts spécifiques pour Devin AI :
* Pour la structure de la base de données : "Génère un schéma de base de données MySQL pour un site d'importation de véhicules avec les tables suivantes : Devis, Clients, Commandes, Partenaires, et Documents. Inclus les relations entre tables et des exemples de données pour chaque champ."
* Pour le calcul automatique des coûts : "Créer un algorithme en JavaScript qui calcule le prix total d'un véhicule importé en fonction de : prix d'achat (en devise originale). Frais de transport (variable selon le pays). Droits de douane ([pays], ex: 10% pour l'UE). TVA locale (ex: 20% en France). Frais d'homologation (forfait de 500€). Affiche le résultat dans une modal avec un récapitulatif détaillé."
* Pour le processus : "Rédige un guide étape par étape du processus (format blog) pour expliquer la prestation d'import pour une voiture. Liste des étapes (1. PRISE DE CONTACT, 2. RECHERCHE PERSONNALISÉE, 3. VALIDATION DU VÉHICULE, 4. IMPORTATION DU VÉHICULE, 5.CONTRÔLE TECHNIQUE, 6. RESTITUTION / LIVRAISON, 7. DEMARCHES ADMINISTRATIVES) délais moyens pour chaque étape (achat, transport, douane, homologation). Coûts cachés à anticiper (ex: frais de stockage au port). Liens vers les sites officiels (douanes, ministères)."