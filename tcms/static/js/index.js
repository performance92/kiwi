import { pageBugsGetReadyHandler } from '../../bugs/static/bugs/js/get'
import { pageBugsMutableReadyHandler } from '../../bugs/static/bugs/js/mutable'
import { pageBugsSearchReadyHandler } from '../../bugs/static/bugs/js/search'

import { pageTestcasesCloneReadyHandler } from '../../testcases/static/testcases/js/clone'
import { pageTestcasesGetReadyHandler } from '../../testcases/static/testcases/js/get'
import { pageTestcasesMutableReadyHandler } from '../../testcases/static/testcases/js/mutable'
import { pageTestcasesSearchReadyHandler } from '../../testcases/static/testcases/js/search'

import { pageTestplansGetReadyHandler } from '../../testplans/static/testplans/js/get'
import { pageTestplansMutableReadyHandler } from '../../testplans/static/testplans/js/mutable'
import { pageTestplansSearchReadyHandler } from '../../testplans/static/testplans/js/search'

import { pageTestrunsEnvironmentReadyHandler } from '../../testruns/static/testruns/js/environment'
import { pageTestrunsGetReadyHandler } from '../../testruns/static/testruns/js/get'
import { pageTestrunsMutableReadyHandler } from '../../testruns/static/testruns/js/mutable'
import { pageTestrunsSearchReadyHandler } from '../../testruns/static/testruns/js/search'

import { pageManagementBuildAdminReadyHandler } from '../../management/static/management/js/build_admin'

const pageHandlers = {
    'page-bugs-get': pageBugsGetReadyHandler,
    'page-bugs-mutable': pageBugsMutableReadyHandler,
    'page-bugs-search': pageBugsSearchReadyHandler,

    'page-testcases-clone': pageTestcasesCloneReadyHandler,
    'page-testcases-get': pageTestcasesGetReadyHandler,
    'page-testcases-mutable': pageTestcasesMutableReadyHandler,
    'page-testcases-search': pageTestcasesSearchReadyHandler,

    'page-testplans-get': pageTestplansGetReadyHandler,
    'page-testplans-mutable': pageTestplansMutableReadyHandler,
    'page-testplans-search': pageTestplansSearchReadyHandler,

    'page-testruns-environment': pageTestrunsEnvironmentReadyHandler,
    'page-testruns-get': pageTestrunsGetReadyHandler,
    'page-testruns-mutable': pageTestrunsMutableReadyHandler,
    'page-testruns-search': pageTestrunsSearchReadyHandler
}

$(() => {
    const body = $('body')
    const pageId = body.attr('id')
    const readyFunc = pageHandlers[pageId]
    if (readyFunc) {
        readyFunc()
    }

    // this page doesn't have a page id
    if ( body.hasClass('grp-change-form') && body.hasClass('management-build') ) {
        pageManagementBuildAdminReadyHandler()
    }
    // todo: add selectpicker() and bootstrapSwitch()
    // initialization here

    // todo: maybe initialize pagination here
})
