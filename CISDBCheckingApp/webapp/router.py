class ReadOnlyRouter:
    def db_for_read(self, model, **hints):
        return 'default'  # or 'prod' if that's what you named your production db

    def db_for_write(self, model, **hints):
        return 'test_db'  # Always route writes to test db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False  # Prevent migrations on production