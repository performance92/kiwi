#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh

assert_up_and_running() {
    sleep 10
    IP_ADDRESS=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kiwi_web`
    # both HTTP and HTTPS display the login page
    rlRun -t -c "curl    -L -o- http://$IP_ADDRESS:8080/  | grep 'Welcome to Kiwi TCMS'"
    rlRun -t -c "curl -k -L -o- https://$IP_ADDRESS:8443/ | grep 'Welcome to Kiwi TCMS'"
}

rlJournalStart
    rlPhaseStartSetup
        # wait for tear-down from previous script b/c
        # in CI subsequent tests can't find the db host
        sleep 5
    rlPhaseEnd

    rlPhaseStartTest "Plain HTTP works"
        rlRun -t -c "docker-compose run -d -e KIWI_DONT_ENFORCE_HTTPS=true --name kiwi_web web /httpd-foreground"
        sleep 10
        rlRun -t -c "docker exec -i kiwi_web /Kiwi/manage.py migrate"
        assert_up_and_running
    rlPhaseEnd

    rlPhaseStartTest "Should not display SSL warning for HTTPS connection"
        rlRun -t -c "docker exec -i kiwi_web /Kiwi/manage.py createsuperuser \
            --username testadmin --email testadmin@domain.com --noinput"
        rlRun -t -c "cat tests/set_testadmin_pass.py | docker exec -i kiwi_web /Kiwi/manage.py shell"
        IP_ADDRESS=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kiwi_web`
        rm -f /tmp/testcookies.txt
        rm -f /tmp/testdata.sslon
        rlRun -t -c "curl -k -L -o- -c /tmp/testcookies.txt https://$IP_ADDRESS:8443/"
        CSRF_TOKEN=`grep csrftoken /tmp/testcookies.txt | cut -f 7`
        rlRun -t -c "curl -e https://$IP_ADDRESS:8443/accounts/login/ -d username=testadmin \
            -d password=password -d csrfmiddlewaretoken=$CSRF_TOKEN -k -L -i -o /tmp/testdata.sslon \
            -b /tmp/testcookies.txt https://$IP_ADDRESS:8443/accounts/login/"
        rlAssertGrep "<title>Kiwi TCMS - Dashboard</title>" /tmp/testdata.sslon
        rlAssertNotGrep "You are not using a secure connection." /tmp/testdata.sslon
    rlPhaseEnd

    rlPhaseStartTest "Should display SSL warning for HTTP connection"
        rm -f /tmp/testcookies.txt
        rlRun -t -c "curl -k -L -o- -c /tmp/testcookies.txt http://$IP_ADDRESS:8080/"
        CSRF_TOKEN=`grep csrftoken /tmp/testcookies.txt | cut -f 7`
        rlRun -t -c "curl -e http://$IP_ADDRESS:8080/accounts/login/ -d username=testadmin \
            -d password=password -d csrfmiddlewaretoken=$CSRF_TOKEN -k -L -i -o /tmp/testdata.ssloff \
            -b /tmp/testcookies.txt http://$IP_ADDRESS:8080/accounts/login/"
        rlAssertGrep "<title>Kiwi TCMS - Dashboard</title>" /tmp/testdata.ssloff
        rlAssertGrep "You are not using a secure connection." /tmp/testdata.ssloff

    rlPhaseStartCleanup
        rlRun -t -c "docker-compose down"
#        rm -f /tmp/testcookies.txt
#        rm -f /tmp/testdata.sslon
        if [ -n "$ImageOS" ]; then
            rlRun -t -c "docker volume rm kiwi_db_data"
        fi
    rlPhaseEnd
rlJournalEnd

rlJournalPrintText
