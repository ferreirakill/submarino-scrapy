from twisted.internet.error import TimeoutError as ServerTimeoutError, DNSLookupError, \
                                   ConnectionRefusedError, ConnectionDone, ConnectError, \
                                   ConnectionLost, TCPTimedOutError
from twisted.internet.defer import TimeoutError as UserTimeoutError

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
import json
import re


class RetryMiddleware(object):

    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (ServerTimeoutError, UserTimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError,
                           IOError,
                           KeyError)

    def __init__(self, settings):
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.max_retry_wrong_uuid = 10
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):        
        if 'dont_retry' in request.meta:
            print 'dont retry in meta'
            return response
        #print "response.status = %s" % (response.status)
        uuids = re.findall('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', response.body)
        #print "uuids: %s" % (uuids)
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        #elif len((json.JSONDecoder().decode(json.loads(response.body)))[0])>1:
        #    ##tenta inserir verificacao aqui
        #    preco_list = json.JSONDecoder().decode(json.loads(response.body))
        #    reason = response_status_message(400)
        #    return self._retry(request, reason, spider) or response
        elif uuids[0]=='00000000-0000-0000-0000-000000000000':
            retries_uuid = request.meta.get('retry_times_uuid', 0) + 1
            if retries_uuid <= self.max_retry_wrong_uuid:
                request.meta['retry_times_uuid'] = retries_uuid
                print "uuids error!: %s" % (uuids)
                print "uuids retry count: %s" % (retries_uuid)
                reason = response_status_message(400)
                return self._retry(request, reason, spider) or response
                
        return response

    def process_exception(self, request, exception, spider):
        print "exception to retry: %s" % (exception)
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and 'dont_retry' not in request.meta:
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)