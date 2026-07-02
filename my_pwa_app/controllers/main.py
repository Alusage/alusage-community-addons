import json
from odoo import http
from odoo.http import request


class MyPWAController(http.Controller):

    @http.route('/my-pwa-app', type='http', auth='user', website=True)
    def index(self):
        """
        Route principale de l'application PWA.
        Authentification requise (auth='user') - redirection automatique vers /web/login si non connecté.
        """
        # Vérifier que l'utilisateur a les droits portal
        if not request.env.user.has_group('base.group_portal') and not request.env.user.has_group('base.group_user'):
            return request.redirect('/web/login?error_message=Access denied')

        # Informations de session pour le frontend
        session_info = {
            'uid': request.env.user.id,
            'name': request.env.user.name,
            'email': request.env.user.email or '',
            'login': request.env.user.login,
            'is_portal': request.env.user.has_group('base.group_portal'),
            'is_internal': request.env.user.has_group('base.group_user'),
        }

        return request.render('my_pwa_app.index', {
            'session_info': json.dumps(session_info),
            'user': request.env.user,
        })

    @http.route('/my-pwa-app/user-info', type='http', auth='user', methods=['GET'])
    def get_user_info(self):
        """
        API endpoint pour récupérer les informations de l'utilisateur connecté.
        Utilisé pour tester la connexion JSON-RPC.
        """
        user = request.env.user

        user_info = {
            'id': user.id,
            'name': user.name,
            'email': user.email or '',
            'login': user.login,
            'is_portal': user.has_group('base.group_portal'),
            'is_internal': user.has_group('base.group_user'),
            'partner_id': user.partner_id.id if user.partner_id else None,
        }

        return request.make_response(
            json.dumps(user_info, ensure_ascii=False),
            headers=[('Content-Type', 'application/json')]
        )