from django.core.files.storage import Storage
from django.conf import settings
from .supabase_client import supabase
from io import BytesIO

class SupabaseStorage(Storage):
    bucket = settings.SUPABASE_BUCKET

    def _save(self, name, content):
        content.seek(0)

        supabase.storage.from_(self.bucket).upload(
            path=name,
            file=content.read(),
            file_options={"upsert": "true"},
        )

        return name

    def exists(self, name):
        # Supabase doesn't support direct exists check
        return False

    def url(self, name):
        return supabase.storage.from_(self.bucket).get_public_url(name)

    def delete(self, name):
        supabase.storage.from_(self.bucket).remove([name])

    def size(self, name):
        return 0

    def open(self, name, mode="rb"):
        raise NotImplementedError("File reading not supported")
