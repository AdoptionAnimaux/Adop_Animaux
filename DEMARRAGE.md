# Guide de démarrage manuel - Microservices avec Traefik

## ✅ Installation terminée !

Consul et Traefik sont maintenant installés dans le dossier `bin/`.

---

---

## 🏠 Test à la Maison (Sur 1 seul PC)

Si vous testez tout seul sur votre PC, vous devez dire aux services d'utiliser "localhost" pour l'enregistrement. **Dans chaque terminal de service**, faites ceci :

```powershell
# 1. Activez le mode local
$env:USE_LOCALHOST="true"

# 2. Lancez le service normalement
python manage.py runserver 8001
```

---

## 🚀 Démarrage des services

**IMPORTANT** : Vous devez ouvrir **6 terminaux PowerShell** et exécuter chaque commande dans un terminal séparé.

### Terminal 1 : Consul
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux
.\bin\consul.exe agent -dev
```
✅ Attendez de voir : `agent: Synced node info`

---

### Terminal 2 : Traefik
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux
.\bin\traefik.exe --configFile=treafik\traefik.yml
```
✅ Attendez de voir : `Configuration loaded from file`

---

### Terminal 3 : Accounts Service (Port 8001)
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux\accounts_service
python manage.py runserver 8001
```
✅ Attendez de voir : `✅ accounts-service enregistré dans Consul`

---

### Terminal 4 : Animals Service (Port 8002)
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux\animals_service
python manage.py runserver 8002
```
✅ Attendez de voir : `✅ animals-service enregistré dans Consul`

---

### Terminal 5 : Adoption Service (Port 8003)
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux\adoption_service
python manage.py runserver 8003
```
✅ Attendez de voir : `✅ adoption-service enregistré dans Consul`

---

### Terminal 6 : Notifications Service (Port 8004)
```powershell
cd c:\Users\prafu\OneDrive\Desktop\Adop_Animaux\notifications_service
python manage.py runserver 8004
```
✅ Attendez de voir : `✅ notifications-service enregistré dans Consul`

---

## 🧪 Vérification

Une fois tous les services démarrés, ouvrez votre navigateur et testez :

1. **Consul UI** : http://localhost:8500/ui
   - Vérifiez que les 4 services sont enregistrés (accounts, animals, adoption, notifications)

2. **Traefik Dashboard** : http://localhost:8080/dashboard/
   - Vérifiez que les routes sont configurées

3. **Test Login** : http://localhost/accounts/login/
   - Connectez-vous avec : `admin@example.com` / `ChangeMe123!`
   - Vous devriez être redirigé vers `/animals/` (le catalogue)

4. **Test Navigation** :
   - Cliquez sur "Catalogue 🐾" dans la navbar
   - Cliquez sur un animal pour voir les détails
   - Cliquez sur "Adopt" pour tester le flux d'adoption

---

## ❌ Dépannage

### Erreur : "Port already in use"
Un service tourne déjà sur ce port. Arrêtez-le avec `Ctrl+C` dans le terminal correspondant.

### Erreur : "Cannot connect to Consul"
Assurez-vous que Consul (Terminal 1) est démarré et affiche `agent: Synced node info`.

### Erreur : "404 Not Found"
Vérifiez que :
- Traefik tourne (Terminal 2)
- Les 4 services Django tournent (Terminaux 3-6)
- Les services sont enregistrés dans Consul (http://localhost:8500/ui)

---

## 📊 Checklist finale

- [ ] Terminal 1 : Consul démarré
- [ ] Terminal 2 : Traefik démarré
- [ ] Terminal 3 : Accounts service (8001) démarré
- [ ] Terminal 4 : Animals service (8002) démarré
- [ ] Terminal 5 : Adoption service (8003) démarré
- [ ] Terminal 6 : Notifications service (8004) démarré
- [ ] Consul UI accessible (http://localhost:8500/ui)
- [ ] Traefik Dashboard accessible (http://localhost:8080/dashboard/)
- [ ] Login fonctionne (http://localhost/accounts/login/)
- [ ] Navigation entre services fonctionne

---

---

## 🌍 Mode Distribué (Multi-PC)

Si vous déployez sur 4 PC différents comme demandé, suivez ces instructions :

### PC 4 : Consul (Leader)
Lancez Consul pour qu'il écoute sur tout le réseau :
```powershell
.\bin\consul.exe agent -server -bootstrap-expect=1 -node=leader -data-dir=consul-data -bind=<IP_PC4> -client=0.0.0.0 -ui
```

### PC 3 : Traefik (Gateway)
Pointez vers le PC 4 :
```powershell
.\bin\traefik.exe --providers.consulcatalog.endpoint.address=<IP_PC4>:8500 --entrypoints.web.address=:80
```

### PC 2 : RabbitMQ + Notifications
1. Installez RabbitMQ sur ce PC.
2. Lancez le service :
```powershell
$env:CONSUL_HOST="<IP_PC4>"
python manage.py runserver <IP_PC2>:8004
```

### PC 1 : Accounts + Animals
Pointez vers PC 4 et PC 2 :
```powershell
$env:CONSUL_HOST="<IP_PC4>"
$env:RABBITMQ_HOST="<IP_PC2>"

# Dans deux terminaux :
python manage.py runserver <IP_PC1>:8001
python manage.py runserver <IP_PC1>:8002
```

---

## 🎉 Succès !
... (reste du fichier)
