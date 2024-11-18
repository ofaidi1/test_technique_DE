

# Projet : Pipeline de Données pour la Gestion des Médicaments et des Publications Scientifiques

## Description du Projet

Ce projet consiste à construire une **pipeline de données** pour traiter des fichiers CSV et JSON contenant des informations sur les médicaments, les essais cliniques et les publications scientifiques. L'objectif est de générer un fichier JSON structuré représentant un graphe de lisaison  entre les médicaments, les publications scientifiques et les journaux, tout en assurant la qualité et la propreté des données.

---
## **Guide d'utilisation :**

### Installer les dépendances
- pip install -r requirements.txt

### Executer la pipeline
- python pipeline.py

### Résultat
- output/drugs_mentions.json

### Traitement Ad-hoc
- choisir le médicament cible dans le fichier config.json
- Les résultats du traitement ad-hoc seront affichés dans le terminal après l'exécution du code.

### Lancer les tests
- pytest tests/ -v



### **Structure du projet :**


```bash
project/
├── src/
│   ├── ingest.py             # Chargement des fichiers CSV et JSON
│   ├── clean.py              # Traitement et nettoyage des données
│   ├── transform.py          # Extraction des mentions et construction du graphe
│   ├── analysis.py           # Analyses spécifiques sur le graphe
│   ├── output.py             # Sauvegarde des résultats JSON
│             
├── data/                     # Les fichiers d'entrée (drugs.csv, pubmed.csv, etc.)
├── output/                   # Le graphe généré (JSON)
├── tests/                    # Tests unitaires
│   ├── test_ingest.py
│   ├── test_clean.py
│   ├── test_transform.py
│   ├── test_output.py
├── .gitignore/               
├── config.json/              # Fichier de cofiguration dans lequel on choisit le médicament pour répondre à la deuxieme question du taitement ad-hoc
├── pipeline.py               # Orchestration complète du pipeline
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation du projet

```

## Conception de la Pipeline de Données

### **1. Modularité**
    - Chaque étape du pipeline est définie dans des fonctions dédiées :

    - 1. **Ingestion** :
    - Chargement des fichiers CSV et JSON tout en gérant automatiquement les encodages pour éviter les erreurs liées aux caractères spéciaux.
    - Grâce à sa conception modulaire, il est facile d'ajouter d'autres sources de données au pipeline.

    2. **Nettoyage** :
    - Suppression des caractères invalides  (comme `\\xc3\\x28`) pour assurer la qualité des données.
    - Unification des formats de dates et gestion des valeurs manquantes.
    - Les fonctions de nettoyage sont génériques et réutilisables, permettant une intégration fluide dans d'autres pipelines.

    3. **Transformation** :
    - Construction de relations hiérarchiques et explicites entre les entités (médicaments, publications et journaux).
    - La modularité de la logique de transformation permet de répondre facilement à de nouveaux besoins ou à des changements dans les spécifications.

    4. **Output** :
    - Génération de fichiers JSON bien structurés et lisibles, avec une gestion optimale des caractères spéciaux grâce à l'utilisation de `ensure_ascii=False`.
    - Le design modulaire permet de personnaliser facilement les formats de sortie ou de les adapter pour les intégrer à d'autres systèmes.

- **Avantages :**
  - Réutilisabilité : Les fonctions peuvent être utilisées pour d'autres pipelines.
  - Lisibilité et maintenabilité : Chaque fonction est simple et se concentre sur une tâche unique.


### **2. Compatibilité avec un Orchestrateur**
- Le pipeline peut être facilement intégré dans un orchestrateur de jobs comme Airflow grâce à sa conception modulaire.
- Chaque étape clé du pipeline (ingestion, nettoyage, transformation, production de résultats) est déjà organisée sous forme de fonctions distinctes, 
  ce qui correspond parfaitement au concept de tâches dans Airflow.
- Le format JSON de sortie est portable et largement compatible.

### **3. Robustesse**
- Gestion des erreurs intégrée :
  - Utilisation de blocs `try-except` pour capturer et journaliser les erreurs, comme les problèmes de chargement de fichiers ou d'encodage.
  - Les erreurs explicites (`ValueError`) facilitent le débogage.


### **4. Scalabilité**
- **Actuel :** Pandas est utilisé pour traiter des volumes de données modérés.
- **Future évolution :** Intégration possible avec PySpark pour les grandes quantités de données.



## Choix des Structures de Données

### 1. **DataFrames pour la Manipulation des Données**
- **Pourquoi ?**
  - Les DataFrames de Pandas permettent une manipulation rapide et efficace des données tabulaires.
  - Ils offrent des fonctionnalités robustes pour le filtrage, la transformation et l'agrégation.


### 2. **Format de l'output Graph JSON **
- **Pourquoi JSON imbriqué ?**
  - Permet une structure qui représente bien le graph de liaison  :
    - Chaque médicament contient une liste de mentions dans des publications scientifiques.
    - Chaque journal contient une liste de médicaments mentionnés.
  - Facile à utiliser pour répondre à des requêtes spécifiques : "Quels journaux mentionnent un médicament donné ?" ou "Quels médicaments sont cités dans un journal ?"



---

## Bonnes Pratiques Python

### **1. Style de Codage**
- Respect des normes PEP 8 :
  - Utilisation de noms explicites pour les variables et fonctions (ex. `clean_data`, `find_mentions`).
  - Limitation des lignes à 79 caractères pour une meilleure lisibilité.

### **2. Documentation**
- Chaque fonction est documentée avec :
  - Une description de son objectif.

### **3. Utilisation de Git**
- Suivi des versions du projet avec Git pour assurer une collaboration efficace et la gestion des modifications.

### **4. Tests**
- Tests unitaires recommandés pour les fonctions clés (ex. `clean_data`, `find_mentions`) afin de garantir la fiabilité.

---



## Amélioration pour traiter des grosses volumétries de données :

Pour gérer des volumes massifs de données (fichiers de plusieurs To ou millions d'enregistrements), plusieurs approches peuvent être envisagées selon le choix des technologies, nous pouvons imaginer 2 solutions :

1. **Utiliser le code Python avec PySpark :**
   - Pour conserver un maximum de contrôle sur le code existant, il est possible de migrer les étapes actuelles vers **PySpark**. 
   - En exécutant PySpark sur **Google Dataproc**, nous bénéficions d'un traitement distribué sur un cluster géré par GCP, tout en réutilisant les transformations Python actuelles.

2. **Utiliser des services managés dans GCP :**
   - Si l'objectif est de minimiser la gestion de l'infrastructure, nous pouvons imaginer une architecture entièrement managée qui utilise les services natifs de GCP, décrite ci-dessous.
### **Architecture Managée avec GCP**

### **1. Stockage des données**
- **Google Cloud Storage (GCS)** :
  - Utilisez un stockage objet évolutif comme GCS pour gérer de gros volumes de fichiers CSV ou JSON.
  - GCS permet une intégration facile avec d'autres services comme BigQuery et Pub/Sub.

---

### **2. Ingestion des données**
- **Architecture Event-Driven :**
  - Configurez une ingestion automatisée basée sur des événements en utilisant **Eventarc** et **Cloud Functions**.
  - Exemple de flux :
    - Lorsqu’un fichier est chargé dans GCS, un événement est déclenché.
    - **Cloud Functions** traite le fichier (validation, nettoyage initial) et l’ingère dans une table brute dans **BigQuery**.

---

### **3. Transformation des données**
- **Transformation avec dbt (Data Build Tool) :**
  - Adoptez **dbt** pour transformer les données dans BigQuery après ingestion.
  - dbt permet :
    - De modéliser les données de manière modulaire et réutilisable.
    - D’assurer la qualité des données grâce à des tests intégrés.
    - D’implémenter différentes stratégies de gestion des données comme :
      - **Modèle incrémental** : Ajouter uniquement les nouvelles données lors de l'exécution du pipeline, sans recharger toute la table.
      - **Snapshot** : Capturer l'état des données à un moment donné pour suivre les modifications historiques.
      - **Full Refresh** : Recharger complètement les données pour les pipelines qui en ont besoin.
  - Ces stratégies permettent d’optimiser les ressources et de gérer les données de manière efficace à grande échelle.


---
### **4. Optimisation dans BigQuery**
Pour garantir des performances optimales avec de grosses volumétries :
- **Partitionnement des tables** :
  - Permet de diviser les données en segments basés sur une colonne spécifique, comme les dates.
  - Réduit le volume de données scannées lors des requêtes, diminuant ainsi les coûts et améliorant les temps de réponse.

- **Clustering des tables** :
  - Organise physiquement les données selon des colonnes fréquemment filtrées ou groupées (par exemple, le nom des médicaments ou des journaux).
  - Améliore la performance des requêtes sur des colonnes spécifiques sans nécessiter un partitionnement supplémentaire.

Ces techniques combinées permettent de maximiser les performances analytiques tout en optimisant les coûts dans BigQuery.


### **5. Orchestration et automatisation**
- **Cloud Composer ou Cloud Workflows :**
  - Utilisez **Cloud Composer** (Airflow géré par GCP) ou **Cloud Workflows** pour orchestrer les étapes de la pipeline :
    - Charger les fichiers depuis GCS.
    - Déclencher les transformations dbt.
    - Charger les résultats transformés dans BigQuery.
  - Avantages :
    - Orchestration fiable avec des tâches parallélisées.
    - Évolutivité automatique pour s’adapter à la charge.

---

## **Résumé des outils GCP proposés**

| Étape                     | Outil GCP                                | Fonctionnalités principales                                              |
|---------------------------|------------------------------------------|--------------------------------------------------------------------------|
| **Stockage**              | Google Cloud Storage (GCS)              | Stockage objet scalable pour des fichiers volumineux.                   |
| **Ingestion**             | Eventarc, Cloud Functions, BigQuery     | Ingestion automatique et stockage dans des tables brutes.               |
| **Transformation**        | dbt, BigQuery                           | Nettoyage et modélisation des données dans BigQuery.                    |
| **Orchestration**         | Cloud Composer, Cloud Workflows         | Orchestration des tâches d’ingestion, transformation et sortie.          |

---

Avec cettes architectures, nous avons le choix entre :
- **Une approche basée sur PySpark et Dataproc** pour conserver un contrôle complet sur le pipeline.
- **Une architecture managée avec les services GCP** pour bénéficier d'une scalabilité automatique et réduire les coûts opérationnels.

Ces options permettent de traiter efficacement des volumes massifs de données tout en répondant aux exigences de performance et de fiabilité.