# !C:\env\391\Scripts\python



import sys
import tkinter as tk  # PEP8: `import *` is not preferred
import os
import argparse
import threading
import queue
from pathlib import Path
from subprocess import Popen
# !C:\env\37\Scripts\python
import json

# include path to labot
sys.path.append(Path(__file__).absolute().parents[1].as_posix())

from labot.logs import logger
from labot.mitm.bridge import *
from labot.gui.gui import *

from fritm import hook, start_proxy_server

FILTER = "port == 5555 || port == 443"

def launch_dofus():
    """to interrupt : dofus.terminate()"""
    platform = sys.platform
    if platform == "darwin":
        path = "/Applications/Dofus.app/Contents/Data/Dofus.app/Contents/MacOS/Dofus"
    elif platform == "win32":
        appdata = os.getenv("appdata")
        parent = os.path.dirname(appdata)
        path = parent + "\\Local\\Ankama\\zaap\\dofus\\Dofus.exe"
    else:
        assert False, (
            "Your platform (%s) doesn't support automated launch yet" % sys.platform
        )
    return Popen(path)


def make_parser():
    parser = argparse.ArgumentParser(
        description="Start the proxy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--server", action="store_true", help="Run a proxy server")
    parser.add_argument(
        "--port", type=int, default=5555, help="Listening port of the proxy server"
    )
    parser.add_argument(
        "--dump-to", type=Path, default=None, help="Capture file (pickle format)"
    )
    parser.add_argument(
        "--launch", action="store_true", help="Launch a new hooked Dofus instance"
    )
    parser.add_argument(
        "--attach", action="store_true", help="Attach to an existing Dofus instance"
    )
    parser.add_argument(
        "--pid",
        type=int,
        default=None,
        help="PID of the Dofus process, only required if there are multiple instances already launched",
    )
    parser.add_argument("--verbose", default="INFO", help="Logging level")
    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    logger.setLevel(args.verbose)

    assert not (args.attach and args.launch), "You cannot both launch and attach"
    if not args.server:
        assert args.dump_to is None, "dump-to not used"
    if not args.attach:
        assert args.pid is None, "pid is not used"

    if args.server:
        bridges = []

        dumper = Dumper(args.dump_to) if args.dump_to else None
        

        def fnQuit():
            sys.exit()
        
        qForm = queue.Queue()
        qSocket = queue.Queue()
        gui = GUI(qForm, qSocket, fnQuit)


        def my_callback(coJeu, coSer):
            global bridges
            global qSocket
            bridge = InjectorBridgeHandler(coJeu, coSer, dumper=dumper, qForm=qForm, qSocket=qSocket)
            bridges.append(bridge)
            bridge.loop()
        t1 = threading.Thread(target=start_proxy_server, args=(my_callback, args.port))
        t1.start()

    if args.launch:
        dofus = launch_dofus()
        target = dofus.pid
                                                                                                                                                         
    if args.attach:
        target = args.pid
        if target is None:
            if sys.platform == "darwin":
                target = "dofus"
            elif sys.platform == "win32":
                target = "Dofus.exe"
            else:
                assert False, "Your platform requires a pid to attach"
        print("Attached")
    if args.launch or args.attach:
        hook(target, args.port, FILTER)
        pass

    if not sys.flags.interactive:
        #sys.exit()
        sys.stdin.read()  # infinite loop
