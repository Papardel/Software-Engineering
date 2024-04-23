class MediaDBRouter:
    """
    A router to control all database operations on models in the
    media_app application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read media_app models go to media_db.
        """
        if model._meta.app_label == 'media_app':
            return 'media_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write media_app models go to media_db.
        """
        if model._meta.app_label == 'media_app':
            return 'media_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the media_app app is involved.
        """
        if obj1._meta.app_label == 'media_app' or \
           obj2._meta.app_label == 'media_app':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the media_app app only appears in the 'media_db'
        database.
        """
        if app_label == 'media_app':
            return db == 'media_db'
        return None