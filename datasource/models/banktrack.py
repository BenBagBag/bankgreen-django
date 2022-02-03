import json
from re import I
import requests
from datetime import datetime, timezone

from django.db import models

import pandas as pd

from datasource.models.datasource import Datasource
from datasource.local.banktrack.secret import PASSWORD as banktrack_password


class Banktrack(Datasource):
    tag_prepend_str = "banktrack_"

    banktrack_link = models.URLField("Link to the banktrack bank page", editable=False)

    @classmethod
    def load_and_create(cls, load_from_api=False):

        # load from api or from local disk.
        df = None
        if not load_from_api:
            print("Loading Banktrack data from local copy...")
            df = pd.read_csv("./datasource/local/banktrack/bankprofiles.csv")
        else:
            print("Loading Banktrack data from API...")
            r = requests.post(
                "https://www.banktrack.org/service/sections/Bankprofile/financedata", data={"pass": banktrack_password}
            )
            res = json.loads(r.text)
            df = pd.DataFrame(res["bankprofiles"])
            df.to_csv("bankprofiles.csv")

        existing_tags = {x.tag for x in cls.objects.all()}
        banks = []
        num_created = 0
        for i, row in df.iterrows():
            num_created, existing_tags = cls._load_or_create_individual_instance(existing_tags, banks, num_created, row)

        return banks, num_created

    @classmethod
    def _load_or_create_individual_instance(cls, existing_tags, banks, num_created, row):
        tag = cls._generate_tag(bt_tag=row.tag, existing_tags=existing_tags)
        source_id = row.tag

        bank, created = Banktrack.objects.update_or_create(
            source_id=source_id,
            defaults={
                'date_updated': datetime.strptime(row.updated_at, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc),
                'banktrack_link': row.link,
                'source_id': source_id,
                'name': row.title,
                'description': row.general_comment,
                'website': row.website,
            },
        )

        if created:
            bank.tag = tag
            bank.save()

        banks.append(bank)
        num_created += 1 if created else 0
        existing_tags.add(tag)
        return num_created, existing_tags

    @classmethod
    def _generate_tag(cls, bt_tag, increment=0, existing_tags=None):
        og_tag = bt_tag

        # memoize existing tags for faster recursion
        if not existing_tags:
            existing_tags = {x.tag for x in cls.objects.all()}

        if increment < 1:
            bt_tag = cls.tag_prepend_str + og_tag
        else:
            bt_tag = cls.tag_prepend_str + og_tag + "_" + str(increment).zfill(2)

        if bt_tag not in existing_tags:
            return bt_tag
        else:
            return cls._generate_tag(og_tag, increment=increment + 1, existing_tags=existing_tags)