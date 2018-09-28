@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
