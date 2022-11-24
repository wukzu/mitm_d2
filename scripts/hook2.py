import select

import fritm


def dumb_callback(soClient, soServer):
    """Forwards all the traffic between the two sockets
    """
    conns = [soClient, soServer]
    other = {soClient: soServer, soServer: soClient}
    print(soClient)
    print(soServer)
    active = True
    try:
        while active:
            rlist, wlist, xlist = select.select(conns, [], conns)
            if xlist or not rlist:
                break
            for r in rlist:
                data = r.recv(8192)
                if not data:
                    active = False
                    break
                print(data)
                other[r].sendall(data)
    finally:
        for c in conns:
            c.close()

fritm.hook("Dofus.exe", 5555)
httpd = fritm.start_proxy_server(dumb_callback, 5555)