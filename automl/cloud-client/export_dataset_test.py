#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

import export_dataset

PROJECT_ID = os.environ["GCLOUD_PROJECT"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)
DATASET_ID = "TEN4058147884539838464"


@pytest.mark.slow
def test_export_dataset(capsys):
    export_dataset.export_dataset(
        PROJECT_ID, DATASET_ID, "gs://{}/TEST_EXPORT_OUTPUT/".format(BUCKET_ID)
    )

    out, _ = capsys.readouterr()
    assert "Dataset exported" in out

    # Delete the created files
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_ID)
    if len(list(bucket.list_blobs(prefix="TEST_EXPORT_OUTPUT"))) > 0:
        for blob in bucket.list_blobs(prefix="TEST_EXPORT_OUTPUT"):
            blob.delete()
