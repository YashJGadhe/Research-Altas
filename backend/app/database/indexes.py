from app.database.database import get_database


async def create_indexes():
    """Create indexes for better query performance"""
    db = get_database()
    
    # Researchers collection indexes
    await db.researchers.create_index([("researcher_key", 1)], unique=True)
    await db.researchers.create_index([("identifiers.orcid", 1)])
    await db.researchers.create_index([("identifiers.scopus_author_id", 1)])
    await db.researchers.create_index([("identifiers.google_scholar_author_id", 1)])
    await db.researchers.create_index([("identifiers.wos_researcher_id", 1)])
    
    # Publications collection indexes
    await db.publications.create_index([("researcher_key", 1)])
    await db.publications.create_index([("platform", 1)])
    await db.publications.create_index([("source_record_id", 1)])
    await db.publications.create_index([("doi", 1)])
    await db.publications.create_index([("publication_year", -1)])
    
    # Compound index for unique publications per platform
    await db.publications.create_index(
        [("researcher_key", 1), ("platform", 1), ("source_record_id", 1)],
        unique=True
    )
    
    # Sync logs indexes
    await db.sync_logs.create_index([("researcher_key", 1)])
    await db.sync_logs.create_index([("synced_at", -1)])
    
    print("Database indexes created successfully")
