# API Documentation
Version: v1.0
Base URL: http://localhost:5000/api/v1.0

This API powers the Sports Match Review Platform. It supports match management, video uploads, comments, teams, and users.

============================================================
AUTHENTICATION (AUTH0)
============================================================

This API uses Auth0 JWT Access Tokens.

Include the token in protected requests:

Authorization: Bearer <access_token>

Role-based access (from Auth0 custom claim):
https://example.com/roles: ["admin"]

ACCESS LEVELS:
- Public: Anyone can view matches, teams, users, comments, videos
- Authenticated: Logged-in users can post comments
- Admin: Users with "admin" role can add/update/delete matches, teams, users, videos, comments

============================================================
MATCHES ENDPOINTS
============================================================

GET /matches?pn={page}&ps={pageSize}
Public
Returns paginated matches.

GET /matches/count
Public
Returns total match count.

GET /matches/{id}
Public
Returns a single match.

POST /matches
Admin only
Headers:
Authorization: Bearer <token>
Body (FormData):
- HomeTeam
- AwayTeam
- Date
- VideoURL (optional)

PUT /matches/{id}
Admin only
Headers:
Authorization: Bearer <token>

DELETE /matches/{id}
Admin only
Headers:
Authorization: Bearer <token>

============================================================
MATCH VIDEO UPLOADS
============================================================

POST /matches/{id}/uploads
Admin only
Headers:
Authorization: Bearer <token>
Body:
FormData containing video file

GET /matches/{id}/uploads
Public
Returns video metadata or URL.

DELETE /matches/{id}/uploads
Admin only
Headers:
Authorization: Bearer <token>

============================================================
COMMENTS ENDPOINTS
============================================================

GET /matches/{id}/comments
Public
Returns comments for a match.

POST /matches/{id}/comments
Authenticated users only
Headers:
Authorization: Bearer <token>
Body (FormData):
- username
- text

DELETE /matches/{matchId}/comments/{commentId}
Admin only
Headers:
Authorization: Bearer <token>

============================================================
TEAMS ENDPOINTS
============================================================

GET /teams?pn={page}&ps={pageSize}
Public
Paginated teams.

GET /teams/count
Public
Total team count.

GET /teams/{id}
Public
Returns a single team.

POST /teams
Admin only
Headers:
Authorization: Bearer <token>
Body (FormData):
- Team
- Division
- Players

PUT /teams/{id}
Admin only
Headers:
Authorization: Bearer <token>

DELETE /teams/{id}
Admin only
Headers:
Authorization: Bearer <token>

============================================================
USERS ENDPOINTS
============================================================

GET /users?pn={page}&ps={pageSize}
Public
Paginated users.

GET /users/count
Public
Total user count.

GET /users/{id}
Public
Returns a single user.

POST /users
Admin only
Headers:
Authorization: Bearer <token>
Body (FormData):
- name
- username
- password
- email
- admin

PUT /users/{id}
Admin only
Headers:
Authorization: Bearer <token>

DELETE /users/{id}
Admin only
Headers:
Authorization: Bearer <token>

============================================================
PAGINATION RULES
============================================================

All paginated endpoints use:
?pn={pageNumber}&ps={pageSize}

============================================================
SUMMARY TABLE
============================================================

GET     /matches                                   Public
GET     /matches/count                             Public
GET     /matches/{id}                              Public
POST    /matches                                   Admin
PUT     /matches/{id}                              Admin
DELETE  /matches/{id}                              Admin

POST    /matches/{id}/uploads                      Admin
GET     /matches/{id}/uploads                      Public
DELETE  /matches/{id}/uploads                      Admin

GET     /matches/{id}/comments                     Public
POST    /matches/{id}/comments                     Authenticated
DELETE  /matches/{id}/comments/{commentId}         Admin

GET     /teams                                     Public
GET     /teams/count                               Public
GET     /teams/{id}                                Public
POST    /teams                                     Admin
PUT     /teams/{id}                                Admin
DELETE  /teams/{id}                                Admin

GET     /users                                     Public
GET     /users/count                               Public
GET     /users/{id}                                Public
POST    /users                                     Admin
PUT     /users/{id}                                Admin
DELETE  /users/{id}                                Admin
