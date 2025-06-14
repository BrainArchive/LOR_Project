
import gspread
from django.core.management.base import BaseCommand
from oauth2client.service_account import ServiceAccountCredentials
from characters.models import Spell, ClassFeat
import json, os
from io import StringIO
# Define the mapping from sheet level to index
LEVEL_MAP = {
    'Cantrips': 0,
    '1st Level': 1,
    '2nd Level': 2,
    '3rd Level': 3,
    '4th Level': 4,
    '5th Level': 5,
    '6th Level': 6,
    '7th Level': 7,
    '8th Level': 8,
    '9th Level': 9,
    '10th Level': 10,
}
from django.db import connection
print("📡 DB ENGINE:", connection.settings_dict['ENGINE'], flush=True)
print("📡 DB NAME:", connection.settings_dict['NAME'], flush=True)


def safe_str(value):
    return value.strip() if isinstance(value, str) else str(value)


class Command(BaseCommand):
    help = "Sync spells and feats from Google Sheets"

    def handle(self, *args, **options):
        print("🟢 SYNC JOB STARTED", flush=True)

        try:
            # Setup auth
            json_creds = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
            if not json_creds:
                print("❌ ERROR: GOOGLE_SHEETS_CREDENTIALS_JSON not set", flush=True)
                return

            creds_dict = json.loads(json_creds)
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            print("✅ Google Sheets client initialized", flush=True)

            # SPELLS
            spell_sheet = client.open_by_key("1tUP5rXleImOKnrOVGBnmxNHHDAyU0HHxeuODgLDX8SM")
            for sheet in spell_sheet.worksheets():
                print(f"📘 Processing sheet: {sheet.title}", flush=True)
                level = LEVEL_MAP.get(sheet.title.strip(), 0)
                rows = sheet.get_all_records()
                print(f"🔢 {len(rows)} rows in {sheet.title}", flush=True)

                for row in rows:
                    row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
                    spell_name = row.get('Spell Name', '').strip()
                    if not spell_name:
                        print("⚠️ Skipping row with no spell name", flush=True)
                        continue

                    Spell.objects.update_or_create(
                        name=spell_name,
                        defaults={
                            'level': level,
                            'classification': safe_str(row.get('Classification', '')),
                            'description': safe_str(row.get('Description', '')),
                            'effect': safe_str(row.get('Effect', '')),
                            'upcast_effect': safe_str(row.get('Upcasted Effect', '')),
                            'saving_throw': safe_str(row.get('Saving Throw', '')),
                            'casting_time': safe_str(row.get('Casting Time', '')),
                            'duration': safe_str(row.get('Duration', '')),
                            'components': safe_str(row.get('Components', '')),
                            'range': safe_str(row.get('Range', '')),
                            'target': safe_str(row.get('Target', '')),
                            'school': safe_str(row.get('School', '')),
                            'origin': safe_str(row.get('Origin', '')),
                            'sub_origin': safe_str(row.get('Sub Origin', '')),
                            'mastery_req': safe_str(row.get('Mastery Req', '')),
                            'tags': safe_str(row.get('Other Tags', '')),
                        }
                    )

            # FEATS
            feat_sheet = client.open_by_key("1-WHN5KXt7O7kRmgyOZ0rXKLA6s6CbaOWFmvPflzD5bQ").sheet1
            rows = feat_sheet.get_all_records()

            for row in rows:
                feat_name = row.get('Feat', '').strip()
                if not feat_name:
                    print("⚠️ Skipping row with no Feat name:", row, flush=True)
                    continue

                raw_type = row.get('Feat Type', '')
                cleaned = raw_type.lower().replace('/', ',').replace('\\', ',')
                parts = [p.strip().capitalize() for p in cleaned.split(',') if p.strip()]
                parts = ['General' if p == 'Racial' else p for p in parts]
                parts = sorted(set(parts), key=lambda x: ['General', 'Class', 'Skill'].index(x) if x in ['General', 'Class', 'Skill'] else x)
                normalized_feat_type = ", ".join(parts)

                ClassFeat.objects.update_or_create(
                    name=safe_str(feat_name),
                    defaults={
                        'description': safe_str(row.get('Description', '')),
                        'level_prerequisite': safe_str(row.get('Level Prerequisite', '')),
                        'feat_type': safe_str(normalized_feat_type),
                        'class_name': safe_str(row.get('Class', '')),
                        'race': safe_str(row.get('Race', '')),
                        'tags': safe_str(row.get('Tags', '')),
                        'prerequisites': safe_str(row.get('Pre-req', ''))
                    }
                )


            print(f"📦 Total spells: {Spell.objects.count()}", flush=True)
            print(f"📦 Total feats: {ClassFeat.objects.count()}", flush=True)

            print("✅ SYNC JOB DONE", flush=True)
            self.stdout.write(self.style.SUCCESS("Spells and Class Feats synced successfully."))

        except Exception as e:
            print("❌ Exception occurred:", flush=True)
            print(e, flush=True)
            import traceback
            traceback.print_exc()
