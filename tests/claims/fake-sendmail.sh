#!/bin/sh
cat >> /tmp/efy-test-mail
printf '\n--EFY-TEST-MESSAGE--\n' >> /tmp/efy-test-mail
exit "${EFY_TEST_MAIL_EXIT:-0}"
