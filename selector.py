#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import selectors
import socket


def read(p_sock, p_mask):
    pass

sock = socket
sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, read)