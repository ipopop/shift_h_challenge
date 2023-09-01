doc API :

1. Authentification
<<
Toutes les requêtes de l'API doivent être authentifiées à l'aide du token d'API généré via l'interface utilisateur. L'authentification doit être effectuée en incluant le header Authorization: Bearer YOUR_API_TOKEN dans chaque requête.

YOUR_API_TOKEN est une clé unique qui te permettra d'accéder à l'API (générer un token).
>>

2. Limitation des requêtes
<<
Afin de garantir une performance optimale pour tous les utilisateurs de notre API, nous avons instauré une limitation sur le nombre de requêtes qu'un client peut effectuer en l'espace de 10 minutes. Cette limitation est définie comme suit:
NOMBRE DE REQUÊTES MAXIMUM PAR 10 MINUTES = 500

Cela veut dire qu'un utilisateur ne peut pas effectuer plus de 500 requêtes à l'API dans une fenêtre glissante de 10 minutes.

Nous suivons le nombre de requêtes effectuées par chaque client en temps réel. Chaque requête est enregistrée avec une horodatage (created_at). Pour déterminer si un utilisateur a dépassé la limite, nous comptons le nombre de requêtes effectuées dans les 10 dernières minutes.

Si vous dépassez cette limite de requêtes, votre requête sera rejetée et vous recevrez un code d'erreur HTTP approprié, généralement 429 Too Many Requests. Vous devrez alors attendre que certaines de vos requêtes précédentes sortent de la fenêtre de 10 minutes avant de pouvoir effectuer de nouvelles requêtes.

Conseil: Pensez à prendre en compte ces limites dans la création de vos programmes pour ne pas atteindre les limites trop rapidement. Une bonne pratique est d'ajouter un délai de 1 ou 2 secondes entre chaque requête si elles sont effectuées en boucle.
>>

3. Plannings
<<
Les plannings sont la ressource centrale de l'API. Tu peux lister tous les plannings disponibles et filtrer par type.
Lister les plannings (GET /api/v1/plannings)
Endpoint: GET /api/v1/plannings Requête (sans filtre):
curl -X GET "https://shiftheroes.fr/api/v1/plannings" -H "Authorization: Bearer YOUR_API_TOKEN"
Requête (avec filtre de type):
curl -X GET "https://shiftheroes.fr/api/v1/plannings?type=TYPE" -H "Authorization: Bearer YOUR_API_TOKEN"
Réponse:
[ { "id": "X05fNV", "planning_type": "daily", "state": "available", "published_at": "2023-07-07T08:46:45.215Z" }, { "id": "e6bdK2", "planning_type": "permanent", "state": "available", "published_at": "2023-07-07T08:37:54.353Z" }, { "id": "j9KDf4", "planning_type": "weekly", "state": "available", "published_at": "2023-07-07T08:47:58.611Z" } ]

Astuce : Utilisez le paramètre ?type=TYPE pour filtrer les plannings selon leur type (permanent, daily, weekly).
>>

4. Shifts
<<
Lister les créneaux d'un planning (GET /api/v1/plannings/:planning_id/shifts)
Endpoint: GET /api/v1/plannings/:planning_id/shifts Requête:
curl -X GET "https://shiftheroes.fr/api/v1/plannings/:planning_id/shifts" -H "Authorization: Bearer YOUR_API_TOKEN"
Réponse:
[ { "id": "lqQFnY", "day": "mardi", "start_hour": "2000-01-01T08:00:00.000Z", "end_hour": "2000-01-01T14:00:00.000Z", "seats": 10, "seats_taken": 1 }, { "id": "x2OFW1", "day": "lundi", "start_hour": "2000-01-01T08:00:00.000Z", "end_hour": "2000-01-01T14:00:00.000Z", "seats": 12, "seats_taken": 0 } // autres shifts... ]
>>

5. Reservations
<<
Lister ses réservations sur un planning (GET /api/v1/plannings/:planning_id/reservations)
Endpoint: GET /api/v1/plannings/:planning_id/reservations Requête:
curl -X GET "https://shiftheroes.fr/api/v1/plannings/:planning_id/reservations" -H "Authorization: Bearer YOUR_API_TOKEN"
Réponse:
[ { "id": 103, "user_id": 5, "shift_id": "lqQFnY" // autres attributs de la réservation... }, { "id": 104, "user_id": 5, "shift_id": "x2OFW1" // autres attributs de la réservation... } // autres réservations... ]
Créer une réservation sur un shift (POST /api/v1/plannings/:planning_id/shifts/:shift_id/reservations)
Endpoint: POST /api/v1/plannings/:planning_id/shifts/:shift_id/reservations Requête:
curl -X POST "https://shiftheroes.fr/api/v1/plannings/:planning_id/shifts/:shift_id/reservations" -H "Authorization: Bearer YOUR_API_TOKEN"
Réponse: La réservation est créée avec succès.
Supprimer une réservation (DELETE /api/v1/plannings/:planning_id/shifts/:shift_id/reservations/:reservation_id)
Endpoint: DELETE /api/v1/plannings/:planning_id/shifts/:shift_id/reservations/:reservation_id Requête:
curl -X DELETE "https://shiftheroes.fr/api/v1/plannings/:planning_id/shifts/:shift_id/reservations/:reservation_id" -H "Authorization: Bearer YOUR_API_TOKEN"
Réponse: La réservation est supprimée avec succès.
>>