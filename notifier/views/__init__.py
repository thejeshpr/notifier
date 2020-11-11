from notifier.db import SessionLocal, engine, models

# models.Base.metadata.drop_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    acquire db connection on need basis
    """
    try:
        db = SessionLocal()
        yield db
    finally:        
        db.close()