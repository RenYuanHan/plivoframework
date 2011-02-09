# -*- coding: utf-8 -*-
"""
Outbound server example in async mode full .
"""

from telephonie.core.outboundsocket import (OutboundEventSocket, OutboundServer)
from telephonie.utils.logger import StdoutLogger
import gevent.queue
import gevent


class AsyncOutboundEventSocket(OutboundEventSocket):
    def __init__(self, socket, address, log, filter=None):
        self.log = log
        self._action_queue = gevent.queue.Queue()
        OutboundEventSocket.__init__(self, socket, address, filter)

    def _protocol_send(self, command, args=""):
        self.log.info("[%s] args='%s'" % (command, args))
        response = super(AsyncOutboundEventSocket, self)._protocol_send(command, args)
        self.log.info(str(response))
        return response

    def _protocol_sendmsg(self, name, args=None, uuid="", lock=False, loops=1):
        self.log.info("[%s] args=%s, uuid='%s', lock=%s, loops=%d" \
                      % (name, str(args), uuid, str(lock), loops))
        response = super(AsyncOutboundEventSocket, self)._protocol_sendmsg(name, args, uuid, lock, loops)
        self.log.info(str(response))
        return response

    def on_channel_execute_complete(self, event):
        if event.getHeader('Application') == 'playback':
            self._action_queue.put(event)

    def on_channel_answer(self, event):
<<<<<<< HEAD
        self.log.info("Channel answered")
=======
        gevent.sleep(1) # sleep 1 sec: sometimes sound is truncated after answer 
        self._action_queue.put(event)
>>>>>>> parent of 3e39384... fix outbound sync/async server examples

    def run(self):
        self.log.info("Channel Unique ID => %s" % self.get_channel_unique_id())

        # only catch events for this channel
        self.myevents()
        # answer channel
        self.answer()
<<<<<<< HEAD
=======
        self.log.info("Wait answer")
        event = self._action_queue.get(timeout=20)
        self.log.info("Channel answered")

>>>>>>> parent of 3e39384... fix outbound sync/async server examples
        # play file
        self.playback("/usr/local/freeswitch/sounds/en/us/callie/ivr/8000/ivr-hello.wav", terminators="*")
        # wait until playback is done
        self.log.info("Waiting end of playback ...")
        event = self._action_queue.get()
        # log playback execute response
        self.log.info("Playback done (%s)" % str(event.getHeader('Application-Response')))
        # finally hangup
        self.hangup()


class AsyncOutboundServer(OutboundServer):
    def __init__(self, address, handle_class, filter=None):
        self.log = StdoutLogger()
        self.log.info("Start server %s ..." % str(address))
        OutboundServer.__init__(self, address, handle_class, filter)

    def do_handle(self, socket, address):
        self.log.info("New request from %s" % str(address))
        self._handle_class(socket, address, self.log, filter=self._filter)
        self.log.info("End request from %s" % str(address))



if __name__ == '__main__':
    outboundserver = AsyncOutboundServer(('127.0.0.1', 8084), AsyncOutboundEventSocket)
    outboundserver.serve_forever()

