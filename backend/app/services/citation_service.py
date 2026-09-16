"""
ResearchAtlas - Citation Service

Business logic for citation management operations.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId

from app.database.database import get_collection
from app.models.citation import CitationRecord, CitationHistory, CitationFetchLog


class CitationService:
    """Service for citation management operations."""
    
    def __init__(self):
        self.records_collection = CitationRecord.COLLECTION_NAME
        self.history_collection = CitationHistory.COLLECTION_NAME
        self.logs_collection = CitationFetchLog.COLLECTION_NAME
    
    def _get_records_collection(self):
        return get_collection(self.records_collection)
    
    def _get_history_collection(self):
        return get_collection(self.history_collection)
    
    def _get_logs_collection(self):
        return get_collection(self.logs_collection)
    
    async def get_all_records(self) -> List[Dict]:
        """Get all citation records."""
        collection = self._get_records_collection()
        cursor = collection.find({}).sort("faculty_name", 1)
        records = await cursor.to_list(length=None)
        return [CitationRecord.to_response(record) for record in records]
    
    async def get_record_by_id(self, record_id: str) -> Optional[Dict]:
        """Get a citation record by ID."""
        collection = self._get_records_collection()
        try:
            record = await collection.find_one({"_id": ObjectId(record_id)})
            if record:
                return CitationRecord.to_response(record)
            return None
        except Exception:
            return None
    
    async def get_record_by_faculty_id(self, faculty_id: str) -> Optional[Dict]:
        """Get a citation record by faculty ID."""
        collection = self._get_records_collection()
        record = await collection.find_one({"faculty_id": faculty_id})
        if record:
            return CitationRecord.to_response(record)
        return None
    
    async def update_record(
        self,
        record_id: str,
        update_data: Dict[str, Any],
        updated_by: str,
        change_source: str = "manual",
        source_platform: str = "MANUAL"
    ) -> Optional[Dict]:
        """
        Update a citation record with history tracking.
        
        Creates a snapshot of old data before updating if there are changes.
        """
        collection = self._get_records_collection()
        
        try:
            # Get current record
            current_record = await collection.find_one({"_id": ObjectId(record_id)})
            if not current_record:
                return None
            
            # Compare and detect changes
            changed_fields = self._detect_changes(current_record, update_data)
            
            # If there are changes, create history snapshot
            if changed_fields:
                snapshot = self._create_snapshot(current_record, changed_fields)
                await self._create_history_record(
                    citation_record_id=record_id,
                    faculty_id=current_record["faculty_id"],
                    faculty_name=current_record["faculty_name"],
                    snapshot=snapshot,
                    changed_fields=changed_fields,
                    change_source=change_source,
                    source_platform=source_platform,
                    created_by=updated_by
                )
            
            # Update the record
            update_data["updated_at"] = datetime.utcnow()
            update_data["updated_by"] = updated_by
            
            if change_source == "api":
                update_data["last_fetched_at"] = datetime.utcnow()
            
            result = await collection.find_one_and_update(
                {"_id": ObjectId(record_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                return CitationRecord.to_response(result)
            return None
            
        except Exception as e:
            print(f"[ERROR] Failed to update citation record: {str(e)}")
            return None
    
    def _detect_changes(self, current: Dict, update_data: Dict) -> List[str]:
        """Detect which fields have changed."""
        changed_fields = []
        
        # Check metrics fields
        metrics_fields = [
            ("web_of_science", ["papers", "citations", "h_index"]),
            ("scopus", ["papers", "citations", "h_index"]),
            ("google_scholar", ["papers", "citations", "h_index", "i10_index"])
        ]
        
        for source, fields in metrics_fields:
            if source in update_data and update_data[source]:
                current_source = current.get(source, {})
                update_source = update_data[source]
                
                for field in fields:
                    if field in update_source:
                        current_value = current_source.get(field, 0)
                        new_value = update_source[field]
                        
                        if current_value != new_value:
                            changed_fields.append(f"{source}.{field}")
        
        # Check URL fields
        url_fields = [
            "publons_url", "scopus_url", "google_scholar_url", "researchgate_url"
        ]
        
        for field in url_fields:
            if field in update_data:
                current_value = current.get(field, "")
                new_value = update_data[field]
                
                if current_value != new_value:
                    changed_fields.append(field)
        
        # Check ORCID and OpenAlex
        if "orcid" in update_data and update_data["orcid"]:
            current_orcid = current.get("orcid", {})
            update_orcid = update_data["orcid"]
            
            for field in ["id", "url"]:
                if field in update_orcid:
                    if current_orcid.get(field, "") != update_orcid[field]:
                        changed_fields.append(f"orcid.{field}")
        
        if "openalex" in update_data and update_data["openalex"]:
            current_openalex = current.get("openalex", {})
            update_openalex = update_data["openalex"]
            
            for field in ["id", "url"]:
                if field in update_openalex:
                    if current_openalex.get(field, "") != update_openalex[field]:
                        changed_fields.append(f"openalex.{field}")
        
        return changed_fields
    
    def _create_snapshot(self, record: Dict, changed_fields: List[str]) -> Dict:
        """Create a snapshot of the current record for history."""
        snapshot = {}
        
        # Extract only the changed fields
        for field_path in changed_fields:
            parts = field_path.split(".")
            
            if len(parts) == 1:
                # Top-level field
                snapshot[field_path] = record.get(field_path)
            elif len(parts) == 2:
                # Nested field (e.g., "web_of_science.papers")
                source, field = parts
                if source not in snapshot:
                    snapshot[source] = {}
                snapshot[source][field] = record.get(source, {}).get(field)
        
        return snapshot
    
    async def _create_history_record(
        self,
        citation_record_id: str,
        faculty_id: str,
        faculty_name: str,
        snapshot: Dict,
        changed_fields: List[str],
        change_source: str,
        source_platform: str,
        created_by: Optional[str] = None
    ):
        """Create a history record."""
        history_collection = self._get_history_collection()
        
        history_doc = CitationHistory.create_snapshot(
            citation_record_id=citation_record_id,
            faculty_id=faculty_id,
            faculty_name=faculty_name,
            snapshot=snapshot,
            changed_fields=changed_fields,
            change_source=change_source,
            source_platform=source_platform,
            created_by=created_by
        )
        
        await history_collection.insert_one(history_doc)
    
    async def get_history_by_faculty_id(self, faculty_id: str) -> List[Dict]:
        """Get citation history for a faculty member."""
        history_collection = self._get_history_collection()
        cursor = history_collection.find({"faculty_id": faculty_id}).sort("created_at", -1)
        records = await cursor.to_list(length=None)
        return [CitationHistory.to_response(record) for record in records]
    
    async def create_fetch_log(
        self,
        faculty_id: str,
        faculty_name: str,
        source: str,
        status: str,
        started_at: datetime,
        completed_at: Optional[datetime] = None,
        records_found: int = 0,
        records_updated: int = 0,
        error_message: Optional[str] = None,
        triggered_by: Optional[str] = None
    ):
        """Create a fetch log entry."""
        logs_collection = self._get_logs_collection()
        
        log_doc = CitationFetchLog.create_log(
            faculty_id=faculty_id,
            faculty_name=faculty_name,
            source=source,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            records_found=records_found,
            records_updated=records_updated,
            error_message=error_message,
            triggered_by=triggered_by
        )
        
        await logs_collection.insert_one(log_doc)
    
    async def get_fetch_logs(self, faculty_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get fetch logs."""
        logs_collection = self._get_logs_collection()
        
        query = {}
        if faculty_id:
            query["faculty_id"] = faculty_id
        
        cursor = logs_collection.find(query).sort("started_at", -1).limit(limit)
        records = await cursor.to_list(length=None)
        return [CitationFetchLog.to_response(record) for record in records]
