from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Inspect database schema'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check accounts_userprofile table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'accounts_userprofile'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            self.stdout.write("Accounts UserProfile table structure:")
            for column in columns:
                self.stdout.write(f"  {column[0]} ({column[1]}) - Nullable: {column[2]}")