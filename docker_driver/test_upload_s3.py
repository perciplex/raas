from datetime import datetime

import upload_s3_utils

test_fname = "test_{}.json".format(datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
print("\nTrying to upload test file {} now...".format(test_fname))
upload_s3_utils.upload_results("/tmp/log.json", test_fname)

print("\nUploaded!")
