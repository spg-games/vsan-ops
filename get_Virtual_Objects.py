import vsanapiutils
import argparse
import sys
import ssl
from pyVim.connect import vim, SmartConnect, Disconnect
from pyVmomi import pbm, VmomiSupport
from tabulate import tabulate

def mk_view_ref(si, obj_type):
    container = si.content.rootFolder
    view_ref = si.content.viewManager.CreateContainerView(
        container=container,
        type=obj_type,
        recursive=True)
    return view_ref

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', required=True)
  parser.add_argument('-u','--user', required=True)
  parser.add_argument('-p','--password', required=True)
  parser.add_argument('-c','--cluster', default=None)
  parser.add_argument('--port', default=443)
  args = parser.parse_args()
  
  # For python 2.7.9 and later, the default SSL context has more strict
  # connection handshaking rule. We may need turn off the hostname checking
  # and client side cert verification.
  context = None
  if sys.version_info[:3] > (2,7,8):
     context = ssl.create_default_context()
     context.check_hostname = False
     context.verify_mode = ssl.CERT_NONE
  
  si = SmartConnect(host=args.host,
                    user=args.user,
                    pwd=args.password,
                    port=int(args.port),
                    sslContext=context)
  
  apiVersion = vsanapiutils.GetLatestVmodlVersion(args.host)
 
  clusters = mk_view_ref(si, [vim.ComputeResource]).view 


  vcMos = vsanapiutils.GetVsanVcMos(si._stub, context=context, version=apiVersion)
  vsanObjSys = vcMos['vsan-cluster-object-system']
  for obj in clusters:
    if obj.name == args.cluster or args.cluster is None:
      objinfo = vsanObjSys.VsanQueryObjectIdentities(cluster=obj, includeHealth=True)
      print(objinfo)
      objinfos = []
      for oi in objinfo.identities:
        objinfos.append(oi.__dict__)
      print(tabulate(objinfos, headers='keys'))
