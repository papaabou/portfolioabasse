import os
import django

# DJANGO BOOTSTRAP
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
django.setup()

from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
import random
import uuid
from decimal import Decimal, Decimal as D
from django.db import IntegrityError, transaction
from django.db import models as dj_models


EXCLUDED_MODEL_LABELS = {
    "contenttypes.contenttype",
    "auth.permission",
    "admin.logentry",
    "sessions.session",
    "django_migrations",
}


def safe_value_for_field(field, fake):
    if isinstance(field, (dj_models.CharField, dj_models.SlugField)):
        max_len = getattr(field, "max_length", 40) or 40
        text = fake.sentence(nb_words=3).strip(".")
        if len(text) > max_len:
            text = text[: max_len - 4]
        if isinstance(field, dj_models.SlugField):
            return slugify(text)[:max_len]
        return text[:max_len]

    if isinstance(field, dj_models.TextField):
        return "\n\n".join(fake.paragraphs(nb=3))

    if isinstance(field, dj_models.EmailField):
        return fake.unique.email()

    if isinstance(field, dj_models.URLField):
        return fake.url()

    if isinstance(field, dj_models.BooleanField):
        return random.choice([True, False])

    if isinstance(field, (dj_models.IntegerField, dj_models.SmallIntegerField, dj_models.PositiveIntegerField, dj_models.PositiveSmallIntegerField)):
        return random.randint(0, 100)

    if isinstance(field, dj_models.FloatField):
        return random.random() * 100

    if isinstance(field, dj_models.DecimalField):
        max_digits = field.max_digits or 8
        decimal_places = field.decimal_places or 2
        value = Decimal(random.uniform(0, 10000)).quantize(D(("1." + "0" * decimal_places)))
        return value

    if isinstance(field, (dj_models.DateField,)):
        return fake.date_this_decade(before_today=True, after_today=False)

    if isinstance(field, (dj_models.DateTimeField,)):
        return fake.date_time_this_decade(before_now=True, after_now=False)

    if isinstance(field, dj_models.TimeField):
        return fake.time()

    # Fallback
    return None


def run():
    if not settings.DEBUG:
        raise Exception("Seeding blocked outside DEBUG mode. Set DEBUG=True to run this script.")

    fake = Faker()
    Faker.seed(2024)
    random.seed(2024)

    User = get_user_model()

    print("Starting full-project seeding using Faker...")

    # Collect all managed, non-proxy models
    all_models = [m for m in apps.get_models() if m._meta.managed and not m._meta.proxy]
    # Filter obvious internal tables
    all_models = [m for m in all_models if f"{m._meta.app_label}.{m._meta.model_name}" not in EXCLUDED_MODEL_LABELS]

    created = {}  # model -> list of instances

    # Clear tables (dangerous but intended for a dev DB)
    print("Clearing existing data for managed models (skipping auth groups/permissions)...")
    for m in reversed(all_models):
        try:
            m.objects.all().delete()
        except Exception:
            pass

    # Create a primary user
    if not User.objects.filter(username="seed_user").exists():
        try:
            User.objects.create_superuser(username="seed_user", email="seed@example.com", password="password")
        except Exception:
            try:
                User.objects.create_user(username="seed_user", email="seed@example.com", password="password")
            except Exception:
                pass

    # Helper to get existing instances for a model
    def existing_for(model):
        return created.get(model, list(model.objects.all()))

    # We'll perform multiple passes to satisfy FK ordering
    pending = set(all_models)
    max_passes = 6
    pass_no = 0
    while pending and pass_no < max_passes:
        pass_no += 1
        progressed = False
        for model in list(pending):
            model_label = f"{model._meta.app_label}.{model._meta.model_name}"
            # Skip some builtins
            if model_label in EXCLUDED_MODEL_LABELS:
                pending.discard(model)
                continue

            # Try to create up to 5 instances per model
            created.setdefault(model, [])
            target_count = 5
            to_create = target_count - len(existing_for(model))
            if to_create <= 0:
                pending.discard(model)
                progressed = True
                continue

            can_create_any = False
            for _ in range(to_create):
                field_kwargs = {}
                m2m_fields = []
                skip = False

                for field in model._meta.get_fields():
                    # Skip auto / reverse relations
                    if getattr(field, 'auto_created', False) and not getattr(field, 'concrete', True):
                        continue

                    if isinstance(field, dj_models.ManyToManyField):
                        m2m_fields.append(field)
                        continue

                    if not getattr(field, 'editable', True) and not isinstance(field, dj_models.ForeignKey):
                        continue

                    if isinstance(field, dj_models.ForeignKey):
                        rel_model = field.remote_field.model
                        rel_instances = existing_for(rel_model)
                        if rel_instances:
                            field_kwargs[field.name] = random.choice(rel_instances)
                        else:
                            if field.null or field.blank:
                                field_kwargs[field.name] = None
                            else:
                                # Cannot create due to missing FK target
                                skip = True
                                break
                        continue

                    if field.primary_key and getattr(field, 'auto_created', False):
                        continue

                    # Provide a value for common field types
                    val = safe_value_for_field(field, fake)
                    if val is None:
                        if getattr(field, 'has_default', False) or field.blank:
                            continue
                        # Fallback for required unknown fields
                        val = str(uuid.uuid4())[:40]

                    field_kwargs[field.name] = val

                if skip:
                    break

                try:
                    with transaction.atomic():
                        inst = model.objects.create(**field_kwargs)
                        # assign m2m
                        for mm in m2m_fields:
                            rel_model = mm.remote_field.model
                            rels = existing_for(rel_model)
                            if rels:
                                sample = random.sample(rels, k=min(len(rels), random.randint(1, min(3, len(rels)))))
                                getattr(inst, mm.name).set(sample)
                        created[model].append(inst)
                        can_create_any = True
                except IntegrityError:
                    # try again with different data
                    continue
                except Exception:
                    # If model creation consistently fails, skip till next pass
                    skip = True
                    break

            if can_create_any:
                progressed = True
            # If after attempting we have at least one instance, consider progress
            if created.get(model):
                pending.discard(model)

        if not progressed:
            # Nothing progressed this pass; avoid infinite loop
            break

    # Summary
    print("Seeding summary:")
    for model, instances in created.items():
        print(f"- {model._meta.app_label}.{model._meta.model_name}: {len(instances)} created")

    print("Done. Run `python faker_seed.py` again to re-run (it clears managed tables).")


if __name__ == '__main__':
    run()
