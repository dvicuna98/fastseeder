class BaseSeed:
    seed_id: str

    def run(self, session):
        raise NotImplementedError("Seed classes must implement `run()` method.")

    def rollback(self, session):
        pass