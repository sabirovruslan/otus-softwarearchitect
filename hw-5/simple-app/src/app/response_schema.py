from app.auth_context import AuthContext


def ctx_profile_schema(ctx: AuthContext) -> dict:
    return {
        'id': ctx.id,
        'first_name': ctx.first_name,
        'last_name': ctx.last_name,
        'phone': ctx.phone,
    }


def health_schema() -> dict:
    return {'status': 'OK'}
