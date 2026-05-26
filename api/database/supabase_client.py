# Supabase Database Client
# Handles briefing caching and retrieval

import os
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """Client for Supabase database operations"""

    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

        self.client: Client = create_client(supabase_url, supabase_key)

    async def save_briefing(
        self,
        region: str,
        briefing_data: Dict[str, Any],
        pdf_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save or update briefing for a region.

        Args:
            region: Geographic region
            briefing_data: Full briefing JSON
            pdf_url: Optional URL to PDF file

        Returns:
            Saved briefing record
        """
        data = {
            "region": region,
            "briefing_data": briefing_data,
            "pdf_url": pdf_url,
            "generated_at": briefing_data.get("generated_at", datetime.now(timezone.utc).isoformat())
        }

        # Upsert: update if exists, insert if not
        # Match on region to ensure only one briefing per region
        result = self.client.table("briefings").upsert(
            data,
            on_conflict="region"
        ).execute()

        return result.data[0] if result.data else None

    async def get_latest_briefing(self, region: str) -> Optional[Dict[str, Any]]:
        """
        Get latest briefing for a region.

        Args:
            region: Geographic region

        Returns:
            Briefing record or None if not found
        """
        result = self.client.table("briefings").select("*").eq(
            "region", region
        ).order("generated_at", desc=True).limit(1).execute()

        return result.data[0] if result.data else None

    async def get_all_briefings(self) -> list[Dict[str, Any]]:
        """
        Get latest briefing for each region.

        Returns:
            List of briefing records (one per region)
        """
        # Get all regions
        regions = ["Middle East", "Indo-Pacific", "Europe/Africa", "Western Hemisphere"]

        briefings = []
        for region in regions:
            briefing = await self.get_latest_briefing(region)
            if briefing:
                briefings.append(briefing)

        return briefings

    async def delete_old_briefings(self, days: int = 30) -> int:
        """
        Delete briefings older than specified days.

        Args:
            days: Number of days to keep

        Returns:
            Number of deleted records
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        result = self.client.table("briefings").delete().lt(
            "generated_at", cutoff_date.isoformat()
        ).execute()

        return len(result.data) if result.data else 0
